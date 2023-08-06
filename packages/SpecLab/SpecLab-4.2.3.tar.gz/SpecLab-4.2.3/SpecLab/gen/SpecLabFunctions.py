import numpy as np
import scipy.interpolate
import scipy.ndimage
import scipy.io
import astropy.io.fits as fits
import matplotlib.pyplot as plt
import sys
from photutils.centroids import centroid_2dg
#from sklearn import mixture
from astropy.io import ascii
import SpecLab.gen.myfunc as mf
from scipy.optimize import leastsq
from scipy.optimize import curve_fit
from scipy.stats import chi2
from scipy import signal
import SpecLab.gen.globals as cnst
# v3.0
# This version of SpecLabFunctions from:  /home/adamkowalski/Dropbox/adam/reduction_scripting/speclab-python/gen





def findind(array,value):
    ''' findind(array, value)'''
    idx = (np.abs(array-value)).argmin()
    return idx


# https://scipy-cookbook.readthedocs.io/items/Rebinning.html
def congrid(a, newdims, method='linear', centre=False, minusone=False):
    '''Arbitrary resampling of source array to new dimension sizes.
    Currently only supports maintaining the same number of dimensions.
    To use 1-D arrays, first promote them to shape (x,1).
    
    Uses the same parameters and creates the same co-ordinate lookup points
    as IDL''s congrid routine, which apparently originally came from a VAX/VMS
    routine of the same name.

    method:
    neighbour - closest value from original data
    nearest and linear - uses n x 1-D interpolations using
                         scipy.interpolate.interp1d
    (see Numerical Recipes for validity of use of n 1-D interpolations)
    spline - uses ndimage.map_coordinates

    centre:
    True - interpolation points are at the centres of the bins
    False - points are at the front edge of the bin

    minusone:
    For example- inarray.shape = (i,j) & new dimensions = (x,y)
    False - inarray is resampled by factors of (i/x) * (j/y)
    True - inarray is resampled by(i-1)/(x-1) * (j-1)/(y-1)
    This prevents extrapolation one element beyond bounds of input array.
    '''
    pass
    if not a.dtype in [n.float64, n.float32]:
        a = n.cast[float](a)

    m1 = n.cast[int](minusone)
    ofs = n.cast[int](centre) * 0.5
    old = n.array( a.shape )
    ndims = len( a.shape )
    if len( newdims ) != ndims:
        print("[congrid] dimensions error. " \
              "This routine currently only support " \
              "rebinning to the same number of dimensions.")
        return None
    print(newdims)
    newdims = n.asarray( newdims, dtype=float )
    dimlist = []
    print(newdims)
    if method == 'neighbour':
        for i in range( ndims ):
            base = n.indices(newdims)[i]
            dimlist.append( (old[i] - m1) / (newdims[i] - m1) \
                            * (base + ofs) - ofs )
        cd = n.array( dimlist ).round().astype(int)
        newa = a[list( cd )]
        return newa

    elif method in ['nearest','linear']:
        # calculate new dims
        for i in range( ndims ):
            base = n.arange( newdims[i] )
            dimlist.append( (old[i] - m1) / (newdims[i] - m1) \
                            * (base + ofs) - ofs )
        # specify old dims
        olddims = [n.arange(i, dtype = n.float) for i in list( a.shape )]

        # first interpolation - for ndims = any
        mint = scipy.interpolate.interp1d( olddims[-1], a, kind=method )
        print(mint)
        print(dimlist[-1])
        newa = mint( dimlist[-1] )

        trorder = [ndims - 1] + range( ndims - 1 )
        for i in range( ndims - 2, -1, -1 ):
            newa = newa.transpose( trorder )

            mint = scipy.interpolate.interp1d( olddims[i], newa, kind=method )
            newa = mint( dimlist[i] )

        if ndims > 1:
            # need one more transpose to return to original dimensions
            newa = newa.transpose( trorder )

        return newa
    elif method in ['spline']:
        oslices = [ slice(0,j) for j in old ]
        oldcoords = n.ogrid[oslices]
        nslices = [ slice(0,j) for j in list(newdims) ]
        newcoords = n.mgrid[nslices]

        newcoords_dims = range(n.rank(newcoords))
        #make first index last
        newcoords_dims.append(newcoords_dims.pop(0))
        newcoords_tr = newcoords.transpose(newcoords_dims)
        # makes a view that affects newcoords

        newcoords_tr += ofs

        deltas = (n.asarray(old) - m1) / (newdims - m1)
        newcoords_tr *= deltas

        newcoords_tr -= ofs

        newa = scipy.ndimage.map_coordinates(a, newcoords)
        return newa
    else:
        print("Congrid error: Unrecognized interpolation type.\n", \
              "Currently only \'neighbour\', \'nearest\',\'linear\',", \
              "and \'spline\' are supported.")
        return None


#https://gist.github.com/zonca/1348792
def rebin(a, new_shape):
    """
    Resizes a 2d array by averaging or repeating elements, 
    new dimensions must be integral factors of original dimensions
    Parameters
    ----------
    a : array_like
        Input array.
    new_shape : tuple of int
        Shape of the output array
    Returns
    -------
    rebinned_array : ndarray
        If the new shape is smaller of the input array, the data are averaged, 
        if the new shape is bigger array elements are repeated
    See Also
    --------
    resize : Return a new array with the specified shape.
    Examples
    --------
    >>> a = np.array([[0, 1], [2, 3]])
    >>> b = rebin(a, (4, 6)) #upsize
    >>> b
    array([[0, 0, 0, 1, 1, 1],
           [0, 0, 0, 1, 1, 1],
           [2, 2, 2, 3, 3, 3],
           [2, 2, 2, 3, 3, 3]])
    >>> c = rebin(b, (2, 3)) #downsize
    >>> c
    array([[ 0. ,  0.5,  1. ],
           [ 2. ,  2.5,  3. ]])
    """
    M, N = a.shape
    m, n = new_shape
    if m<M:
        return a.reshape((m,M/m,n,N/n)).mean(3).mean(1)
    else:
        return np.repeat(np.repeat(a, m/M, axis=0), n/N, axis=1)


def display_fits(image, z1=-99., z2=-99.,resize='No',ytrace = np.zeros(1), ytrace_x = np.zeros(1), xtrace = np.zeros(1), xtrace_y = np.zeros(1), psym='Yes'):
    ''' Call:  display_fits('Image.fits', 
                    [ z1=z1, z2=z2, resize='Yes/No', ytrace = np.zeros(ntrace),
                    ytrace_x = np.zeros(pixel array corresponding to trace), 
                    xtrace =,  xtrace_y=, psym='Yes/No' ] ) 
        Example: 

                    '''
    pass
    
    file = image

    with fits.open(file) as f:
        img = f[0].data

    shp = img.shape

    plt_x = 0
    plt_y = 0
    
    if len(ytrace) > 1:
        xvals_to_plot = np.linspace(0, shp
                                        [1]-1, shp[1])
        yvals_to_plot = ytrace
        plt_y = 1
        if len(ytrace_x) > 1:
            xvals_to_plot = ytrace_x

    if resize == 'Yes':
        img_resize = np.zeros((2048,2048))
        yy = 1024
        while yy < 1024+ 182:
            img_resize[yy,:] = img[yy-1024,:]
            yy=yy+1
        
    if z1 == -99. and z2 == -99.:
        z1 = np.min(img)
        z2 = np.median(img)*1.2
        
    if resize == 'Yes':
        fig=plt.figure(figsize=(7,7))
        im = plt.imshow(img_resize,origin='lower',cmap='bone',vmin=z1,vmax=z2)

    if resize == 'No':
        fig=plt.figure(figsize=(9 ,shp[0]/shp[1] * 9. * 1.35))
        im = plt.imshow(img,origin='lower',cmap='bone',vmin=z1,vmax=z2)
        if plt_y == 1:
            if psym == 'Yes':
                plt.plot(xvals_to_plot, yvals_to_plot,marker='+',ls='dashed',color='black')
            if psym == 'No':
                plt.plot(xvals_to_plot, yvals_to_plot,ls='dashed',color='black')
        if len(xtrace) > 1:
            yvals_to_plot = np.linspace(0, shp[0]-1, shp[0])
            xvals_to_plot = xtrace
            plt_x = 1
            if len(xtrace_x) > 1:
                yvals_to_plot = xtrace_y
            if psym == 'Yes':
                plt.plot(xvals_to_plot, yvals_to_plot,marker='+',ls='dashed',color='black')
            if psym == 'No':
                plt.plot(xvals_to_plot, yvals_to_plot,ls='dashed',color='black')
    plt.show()
    nxx = img.shape[0]
    nyy = img.shape[1]
    print('File [nx , ny] = ',file,'[',nxx,',',nyy,']','   Max = ',np.max(img),'   Median = ',np.median(img))



def polyfit_matr(xvals = np.zeros(1), yvals = np.zeros(1), order=1):
   Z = np.zeros((len(xvals),order+1))
   Z[:,0] = np.float64(1.0)
   k=1
   while k < order+1:
      Z[:,k] = np.float64(xvals**k)
      k = k + 1
      # np.matmul()  np.linalg.inv()   a.transpose()
   beta = np.matmul( np.linalg.inv( np.matmul(Z.transpose(), Z) ), np.matmul(Z.transpose(), yvals) )
   yfit = np.matmul(Z, beta)
   print('returned beta, yfit')
   return beta, yfit
#  Z = dblarr(n_elements(xvals),order+1)

#  Z[*,0] = double(1)
#   for k = 1, order do begin
#      Z[*,k] = xvals^(k)
#   endfor

#   beta = invert(transpose(Z)#Z)#(transpose(Z)#YVALS)
#   yfit = Z#beta
def polyfit_matr_cov(xvals = np.zeros(1), yvals = np.zeros(1), yerr = np.zeros(1), order=1):
   # assuming no covariance elements among y values, this finds the weighted fits and returns their covariance elements.
   Z = np.zeros((len(xvals),order+1))
   Z[:,0] = 1.0
   k=1
   while k < order+1:
      Z[:,k] = xvals**k
      k = k + 1
      # np.matmul()  np.linalg.inv()   a.transpose()
   covy = np.identity(len(yerr)) * yerr**2
   A = np.matmul(Z.transpose(), np.linalg.inv(covy))
   B = np.linalg.inv(np.matmul(A, Z))
   C = np.matmul(Z.transpose(), np.linalg.inv(covy))
   D = np.matmul(C, yvals)
   theta = np.matmul(B, D)
 #  theta = np.matmul( np.linalg.inv( np.matmul(Z.transpose(), Z) ), np.matmul(Z.transpose(), yvals) )
   yfit = np.matmul(Z, theta)
   theta_cov = B

   AA = yvals - np.matmul(Z, theta)
   AAT = AA.T
   BB = yvals - np.matmul(Z, theta)
   kisqr0 = np.matmul(AAT, np.linalg.inv(covy))
   kisqr = np.matmul(kisqr0, BB)
   return theta, theta_cov, yfit, kisqr

def polycreate(betain, xvalsin):
    order = len(betain)
    yvalsout = np.float64(0.0)
    for od in range(order):
      #  print('exponent =',od, 'theta_best =',betain[od])
        yvalsout = yvalsout + np.float64(xvalsin)**(np.float64(od)) * np.float64(betain[od])
    return yvalsout

def bbratio(ratio, lam1, lam2, To):
    # Newton raphson solver of blackbody fit to a ratio of two values.  wavelengths given in angstroms.  ususally coverges in 2 or 3 iteratoins.
    #  See Hawley et al. 1995 for application.
    b = (lam2/lam1)**5
    coeff2 = cnst.HPL * cnst.CCANG / lam2 / cnst.KB
    coeff1 = cnst.HPL * cnst.CCANG / lam1 / cnst.KB

    elim = 1.0
    i=1
    while elim > 1e-3:
        f0 = b * (np.exp(coeff2/To) - 1.0) / (np.exp(coeff1/To) - 1.0) - ratio
        df0 = b / To**2 * (coeff1 * (np.exp(coeff2/To) - 1.0) * np.exp(coeff1/To) / (np.exp(coeff1/To) - 1.0)**2 - coeff2 * np.exp(coeff2/To) / (np.exp(coeff1/To) - 1.0))  # derivative of ratio from wolfram alpha.
        T1 = -1.0*f0 / df0 + To
        elim = np.abs((T1 - To)/To)
        print(i, T1, (T1 - To)/To)
        To = T1
        i+=1
    return T1

def bbNR(wl, fl, To,N_iter=7,elim1=1e-3,elim2=1e-3):
    #  Newton-Raphson solver of a blackbody fit to T and X for a spectrum.
    #  Numerical-Recipes pg. 475
    #  fits to surface flux of blackbody in erg/s/cm2/Ang (ie, planck i_lam multiplied by pi)
    norm1 = np.median(fl)
    norm2 = planck_sflux(np.median(wl), To, 1.0)
    Xo = norm1/norm2
    bbvec = np.vectorize(planck_sflux)
    bbderivvec = np.vectorize(planck_sflux_deriv)

    step1 = 1e2
    step2 = 1e2
    n_iter = 0
    while step1 > elim1 or step2 > elim2:

    # db/dT
        row1 = bbderivvec(wl, To, Xo)
    # db/dX
        row2 = bbvec(wl, To, 1.0)
        F = bbvec(wl, To, Xo) - fl

        Z = np.zeros((len(wl),2))
        Z[:,0] = row1
        Z[:,1] = row2

        eps_matr = np.matmul( np.linalg.inv( np.matmul(Z.transpose(), Z) ), np.matmul(Z.transpose(), -F) )

        T1 = To + eps_matr[0]
        X1 = Xo + eps_matr[1]
        Xo = X1
        To = T1
        step1 = abs(eps_matr[0])/To
        step2 = abs(eps_matr[1])/Xo
        n_iter += 1
        print('Niter = ',n_iter, T1, X1)
        print('Fractional changes in steps:  ',step1, step2)
    
    yfitvals = bbvec(wl, T1, X1)
    print('The converged values of T and X are:  ',T1, X1)
    print('To get the typical value of X, multiply the converged value of X by distance^2 / R_star^2')
    return yfitvals, T1, X1
   
def planck_sflux(inwave, temp, X):  # surface flux of a BB (pi * Blam)
    wl = inwave / 1e8
    Flam = np.pi * X * 2.0 * cnst.HPL * (cnst.CC)**2 / (wl)**5 * 1.0 / (np.exp(cnst.CC * cnst.HPL / (wl * cnst.KB * temp)) - 1.0)  * 1e-8 
    return Flam # erg/s/cm2/Ang


def planck_sflux_deriv(lam, T, X):  # derivative of the planck function, d/dT of erg/s/cm2/Ang
    l1 = lam / 1e8
    deriv = X * np.pi * 2.0 * cnst.CC**3 * cnst.HPL**2 * np.exp( (cnst.CC * cnst.HPL) / (cnst.KB * l1 * T)) / (cnst.KB * T**2 * l1**6 * (np.exp( (cnst.CC * cnst.HPL)/(cnst.KB * T * l1)) - 1.0)**2) * 1e-8
    return deriv

def bincont(xspec, yspec, window_file = 'contwindows.ecsv', errspec= np.zeros(1)):
    windows = ascii.read(window_file)
    nw = len(windows['blue_edge_wl'])
    blue_edge_wl = np.array(windows['blue_edge_wl'])
    red_edge_wl = np.array(windows['red_edge_wl'])
   # good = [False]*len(xspec)
    xtofit = np.zeros(nw)
    ytofit = np.zeros(nw)
    errtofit = np.zeros(nw)
    for ww in range(nw):
        good =  (xspec >= blue_edge_wl[ww]) & (xspec <= red_edge_wl[ww])
        xtofit[ww] = np.mean(xspec[good])
        ytofit[ww] = np.mean(yspec[good])
        if len(errspec) == 1:
            ngood = float(np.count_nonzero(good))
            errtofit[ww] = np.std(yspec[good]) / np.sqrt(ngood)
    return xtofit, ytofit, errtofit



def contfit(xspec, yspec, window_file = 'none', user_sel = 'none',  errspec = np.zeros(1), line_file = False, func = 'poly', corder = 1, printvals = False, sel_n = -99.0, binit=False, xspec_interp = np.zeros(1),sub_val=0.0,Tguess=7500.0,return_parm = False, lam0_guess=6562.8, PLOT = False,linetype='abs',gmaguess=1,find_param_sig=0,plot_covariance = False, dT0=3000.0, perturb_dT0=False, LINE_ADJ_WAVE=0.0, nr_cstep=1.0, return_dict = False):
    '''
    window_file needs a window file created with:   SpecLab.gen_contwindows(blue_arr, red_arr, fname = 'contwindows.X.ecsv')

    Example call for same returned key entries for all types of functions:
       dict_fit = SpecLab.contfit(dat['col1'], dat['col2'], errspec=dat['col3'], return_dict=True)

    func can be the following:  poly, spline3, lorentzian, holtsmark, gaussian, bbcurvefit, bbNR

    user_sel is a conditional statement like '(xspec > 3500) & (xspec < 4000)'
    
    If binit, window_file, or user_sel is set, then probably want to send xspec_interp=xspec to interpolate the yfitvals to all of xspec values (instead of xtofit)
    '''
    # Finished cubic spline (spline3) option for fitting.  npieces = corder.

    # You should use sub_val to subtract minimum of xspec, in the
    #  case of wavelengths, will have precision errors if you dont.
    #  So will fit:  y = m * (x - subval) + b etc.
    # xspec_interp is in case you input binned values, but want to interplate the soln to a finer array of e.g., wavelengths.
    
    # same as polyfit_matr but fits to only select windows.
    if line_file:
        dat = ascii.read(window_file)
        lineid = dat['wid']
        l1 = np.array(dat['l1'])[sel_n] - LINE_ADJ_WAVE
        c1 = np.array(dat['c1'])[sel_n]
        c2 = np.array(dat['c2'])[sel_n] - LINE_ADJ_WAVE
        l2 = np.array(dat['l2'])[sel_n] + LINE_ADJ_WAVE
        c3 = np.array(dat['c3'])[sel_n] + LINE_ADJ_WAVE
        c4 = np.array(dat['c4'])[sel_n]
        blue_edge_wl = np.zeros(2)
        red_edge_wl = np.zeros(2)
        blue_edge_wl[0] = c1
        blue_edge_wl[1] = c3
        red_edge_wl[0] = c2
        red_edge_wl[1] = c4
        nw = 2
        good = [False]*len(xspec)
        for ww in range(nw):
            good = good + np.array( (xspec >= blue_edge_wl[ww]) & (xspec <= red_edge_wl[ww]) )
            xtofit = xspec[good]
            ytofit = yspec[good]
            
    if not line_file:
        #windows = ascii.read(window_file,format='ecsv')
        if window_file == 'none' and user_sel == 'none':
           # print('Fitting to all x and y values')
            blue_edge_wl = np.array([np.min(xspec)])
            red_edge_wl = np.array([np.max(xspec)])
            nw = len(blue_edge_wl)
            good = [False]*len(xspec)
        if window_file == 'none' and user_sel != 'none':
            good = [False]*len(xspec)
        if window_file != 'none' and user_sel == 'none':
            windows = ascii.read(window_file)
            nw = len(windows['blue_edge_wl'])
            blue_edge_wl = np.array(windows['blue_edge_wl'])
            red_edge_wl = np.array(windows['red_edge_wl'])
            good = [False]*len(xspec)
        if not binit:
            if window_file == 'none' and user_sel != 'none':
                good = eval(user_sel)
            else:
                for ww in range(nw):
                    good = good + np.array( (xspec >= blue_edge_wl[ww]) & (xspec <= red_edge_wl[ww]) )
            xtofit = xspec[good]
            ytofit = yspec[good]
            if len(errspec) > 1:
                errtofit = errspec[good]
        if binit:  # user_sel not available here.
            xtofit = np.zeros(nw)
            ytofit = np.zeros(nw)
            errtofit = np.zeros(nw)
            for ww in range(nw):
                good =  (xspec >= blue_edge_wl[ww]) & (xspec <= red_edge_wl[ww])
                xtofit[ww] = np.mean(xspec[good])
                ytofit[ww] = np.mean(yspec[good])
                if len(errspec) > 1:
                    ngood = float(np.count_nonzero(good))
                    errtofit[ww] = np.std(yspec[good]) / np.sqrt(ngood)
    xtofit = xtofit - np.float64(sub_val)  # fit to lambda - lambda0, where lambda0 = sub_val
    if func == 'poly':
        if len(errspec) == 1:
            thetamatr, yfitdum = polyfit_matr(xvals=xtofit, yvals=ytofit, order = corder)
            thetacov = 'n/a'
            dof = float(len(xtofit)) - float(corder + 1)
            chi2 = np.sum( (ytofit - yfitdum)**2 )
            chi2dof = chi2 / dof
            if printvals == True:
                for cc in range(len(thetamatr)):
                    print('Unweighted:  n = {0:.1f}, theta_n = {1:.3e}'.format(cc, thetamatr[cc]))
        else:
            thetamatr, thetacov, yfitdum, chisqrdum = polyfit_matr_cov(xvals=xtofit, yvals=ytofit, yerr=errtofit, order = corder)
            #chisqr1 = np.sum( (ytofit - yfitdum)**2/errtofit**2 )
            chisqr =  chisqrdum
            dof = np.count_nonzero(good) - len(thetamatr)
            chi2dof = chisqr  / dof
            if printvals == True:
                for cc in range(len(thetamatr)):
                    print('n = {0:.1f}, theta_n = {1:.3e}, sigma_theta_n = {2:.3e}'.format(cc, thetamatr[cc], thetacov[cc,cc]**0.5))
                    Q, CHIDISTPDF, CHISQRCDF, pte = mf.chisqrdist(dof, chisqr/dof,reduced=True)
                    pte = chi2.sf(chisqr, dof) # my own pte suffers for very large dof (need to implement gaussian limit) and very
                    # small dof, thus I'm using scipy.stats survival function 
                    print('chi2 = {0:.3f}, chi2/dof = {1:.3f}, dof = {2:.1f}, PTE = {3:.5f}'.format(chisqr, chisqr / dof, dof, pte))
                
        yvalsall = polycreate(thetamatr, xspec - np.float64(sub_val))  # this will be Sprime 
        if len(xspec_interp) > 1:
            yvalsall = polycreate(thetamatr, xspec_interp - np.float64(sub_val))  # if have another array that would like to interpolate to.


    if func == 'bbcurvefit':
        To = 7500.0 # initial guess.
        Planck0 = planck_sflux(np.median(xtofit), To, 1.0)
        guessX = np.median(ytofit) / Planck0
        res2 = scipy.optimize.curve_fit( planck_sflux, xtofit, ytofit, p0=(To, guessX))
        retvals = res2[0]
        planck_sflux_vect = np.vectorize(planck_sflux)
        yvalsall = planck_sflux_vect(xspec, retvals[0], retvals[1])
        print('T_bb = {0:.3e}, X_bb = {1:.3e}'.format(retvals[0], retvals[1]))

    if func == 'bbNR':
        if len(errspec) == 1:
            yvalsall, Tfit, Xfit, success = bbNR(xtofit, ytofit, To=Tguess, cstep=nr_cstep)
            if (success == 0 or np.isfinite(Tfit) == 0 or np.isfinite(Xfit) == 0) and perturb_dT0:
                yvalsall, Tfit, Xfit, success = bbNR(xtofit, ytofit, To=Tguess-dT0, cstep=nr_cstep)
                if success == 0 or np.isfinite(Tfit) == 0 or np.isfinite(Xfit) == 0:
                    yvalsall, Tfit, Xfit, success = bbNR(xtofit, ytofit, To=Tguess-2.0*dT0, cstep=nr_cstep)
                    if success == 0 or np.isfinite(Tfit) == 0 or np.isfinite(Xfit) == 0:
                        yvalsall, Tfit, Xfit, success = bbNR(xtofit, ytofit, To=Tguess-3.0*dT0, cstep=nr_cstep)
                        if success == 0 or np.isfinite(Tfit) == 0 or np.isfinite(Xfit) == 0:
                            yvalsall, Tfit, Xfit, success = bbNR(xtofit, ytofit, To=Tguess-4.0*dT0, cstep=nr_cstep)
                            if success == 0 or np.isfinite(Tfit) == 0 or np.isfinite(Xfit) == 0:
                                yvalsall, Tfit, Xfit, success = bbNR(xtofit, ytofit, To=Tguess-5.0*dT0, cstep=nr_cstep)
                                if success == 0 or np.isfinite(Tfit) == 0 or np.isfinite(Xfit) == 0:
                                    yvalsall, Tfit, Xfit, success = bbNR(xtofit, ytofit, To=Tguess+dT0, cstep=nr_cstep)
                                    if success == 0 or np.isfinite(Tfit) == 0 or np.isfinite(Xfit) == 0:
                                        yvalsall, Tfit, Xfit, success = bbNR(xtofit, ytofit, To=Tguess+2.0*dT0, cstep=nr_cstep)
                                        if success == 0 or np.isfinite(Tfit) == 0 or np.isfinite(Xfit) == 0:
                                            yvalsall, Tfit, Xfit, success = bbNR(xtofit, ytofit, To=Tguess+3.0*dT0, cstep=nr_cstep)
                                            if success == 0 or np.isfinite(Tfit) == 0 or np.isfinite(Xfit) == 0:
                                                yvalsall, Tfit, Xfit, success = bbNR(xtofit, ytofit, To=Tguess+4.0*dT0, cstep=nr_cstep)
                                                if success == 0 or np.isfinite(Tfit) == 0 or np.isfinite(Xfit) == 0:
                                                    yvalsall, Tfit, Xfit, success = bbNR(xtofit, ytofit, To=Tguess+5.0*dT0, cstep=nr_cstep)

            if success == 0 and perturb_dT0:
                print(' (------------) All choices of T0 failed to converge:  ', Tguess-5.0 *dT0, Tguess + 5.0*dT0)
        else:
            yvalsall, Tfit, Xfit, success = bbNR(xtofit, ytofit, To=Tguess, flerr = errtofit)
            if find_param_sig > 0:
                Tfit_arr = np.zeros(find_param_sig)
                Xfit_arr = np.zeros(find_param_sig)
                # perturb the fluxes by random one-sigma values.
                n_dep = len(xtofit)
                n_mc = find_param_sig
                for nc in range(0, n_mc):
                    yfake = np.zeros_like(ytofit)
                    for nx in range(0,n_dep):
                        yfake[nx] = np.random.normal(loc = ytofit[nx], scale = errtofit[nx]) # assume gaussian errors.
                    yfitfake, Tfit_arr[nc], Xfit_arr[nc],success = bbNR(xtofit, yfake, To=Tguess,flerr=errtofit)
                print('Standard deviation of T and X = ',np.std(Tfit_arr - Tfit),np.std(Xfit_arr - Xfit))
                sig_Tfit = np.std(Tfit_arr - Tfit)
                sig_Xfit = np.std(Xfit_arr - Xfit)
                if plot_covariance:
                    f,ax1=plt.subplots()
                    ax1.plot(Xfit_arr, Tfit_arr, marker='+',color='k',ls='none')
                    ax1.plot(Xfit, Tfit, marker='x',color='r')
                    ax1.set_xlim(Xfit - 5.*sig_Xfit, Xfit + 5.*sig_Xfit)
                    ax1.set_ylim(Tfit - 5.*sig_Tfit, Tfit+ 5.*sig_Tfit)
                    plt.savefig('covariance.pdf')
                    plt.show()
        if len(xspec_interp) > 1:
            planckvec = np.vectorize(planck_sflux)
            yvalsall = planckvec(xspec_interp, Tfit, Xfit)
        if return_parm:
            return yvalsall, Tfit, Xfit, success
            
    if func == 'bb_ratio':
        ytofit_norm = ytofit / np.mean(ytofit)
        lam_norm = xtofit[findind(ytofit, np.mean(ytofit))]
        print(lam_norm)
        get_nrsolve = bbratio_n(ytofit_norm, xtofit, lam_norm, 7500.0)
        print('Final solution = ',np.median(get_nrsolve), len(get_nrsolve))
        planck_sflux_vect = np.vectorize(planck_sflux)
        val = np.median(get_nrsolve)
        yvalsall = planck_sflux_vect(xspec,val , np.mean(ytofit_norm))
               
    if func == 'lorentzian':
        parm, yvalsall = mf.fit_lorentz(xtofit,ytofit,abs_ems = linetype,gamma_guess = 1e11,lam0_guess=lam0_guess,xspec_interp = xspec_interp)
    if func == 'lorentzian_noline':
        parm, yvalsall = mf.fit_lorentz_noline(xtofit,ytofit,abs_ems = linetype,gamma_guess = 1e11,lam0_guess=lam0_guess,xspec_interp = xspec_interp)
    if func == 'holtsmark':
        parm, yvalsall = mf.fit_holts(xtofit,ytofit,abs_ems = linetype,gamma_guess = 1e11,lam0_guess=lam0_guess,xspec_interp = xspec_interp)
    if func == 'holtsmark2':
        parm, yvalsall = mf.fit_holts2(xtofit,ytofit,abs_ems = linetype,gamma_guess = 1,lam0_guess=lam0_guess,xspec_interp = xspec_interp)
    if func == 'lorentzian2':
        parm, yvalsall = mf.fit_lorentz2(xtofit,ytofit,abs_ems = linetype,gamma_guess = 1,lam0_guess=lam0_guess,xspec_interp = xspec_interp)
    if func == 'holtsmark3':
        parm, yvalsall = mf.fit_holts3(xtofit,ytofit,abs_ems = linetype,gamma_guess = gmaguess,lam0_guess=lam0_guess,xspec_interp = xspec_interp)

    if func == 'holtsmark3_noline':
        parm, yvalsall = mf.fit_holts3_noline(xtofit,ytofit,abs_ems = linetype,gamma_guess = gmaguess,lam0_guess=lam0_guess,xspec_interp = xspec_interp)
        

        
    if func == 'spline3':
        global NPIECES, MINW, MAXW
        #global x, yvals
        x = np.zeros_like(xtofit) + xtofit  # already has sub_val subtracted.
        yvals = np.zeros_like(ytofit) + ytofit
        NPIECES = corder
        Carr = np.zeros(NPIECES + 3)
        MINW = np.min(xspec_interp - np.float64(sub_val))
        MAXW = np.max(xspec_interp - np.float64(sub_val))
      #  consts = [NPIECES, MINW, MAXW]
        fit = scipy.optimize.curve_fit( spline3n_contfit, x, yvals, p0=Carr )
     #   fit = leastsq( spline3n_fit2, Carr, consts )
        yvalsall = spline3n(xspec_interp - np.float64(sub_val) , fit[0], NPIECES, MINW, MAXW)
        parm = -999
        yfitdum = spline3n(xtofit, fit[0], NPIECES, MINW, MAXW)
        #print('YFIT = ',yfitdum)
       # print('XTOFIT = ',xtofit)
        chi2dof = 1.0
        # YOU MUST SEND XSPEC_INTERP FOR SPLINE3 FITTING.  

    if PLOT:
        rnbw = mf.color_rainbow14()
        f,(ax1,ax3) = plt.subplots(nrows=2,figsize=(8,11))
        ax1.plot(xspec, yspec, color='k')
        ax1.set_xlabel('Wavelength')
       # ax1.set_title('FTS / Observed counts')
        ax1.legend(loc=(0,1.02))
        ax1.plot(xspec_interp, yvalsall, color=rnbw[13])

        ax1.patch.set_visible(False) # hide the 'canvas'

        ax3.plot(xtofit,  (yvalsall - ytofit) / np.std(yvalsall - ytofit),marker='s',color='k',ls='dashed')
        ax3.set_ylim(-5,5)
        ax3.set_ylabel('N sigma')
        #.set_title('rms = ',str(np.std(ratio - ratio_fit_all))
        plt.tight_layout()
        
    if return_dict:
        if len(errspec)==1:
            thetacov = 'n/a'
            errtofit = 'n/a'
        if (func == 'lorentzian' or func == 'gaussian' or func == 'holtsmark' or func == 'spline3'):
            thetamatr = parm
        x0=np.float64(sub_val)

        fit_dict = {'xin':xspec, 'yin':yspec, 'xtofit':xtofit, 'ytofit':ytofit, 'yfit':yfitdum, 'errtofit':errtofit, 'xfitall':xspec_interp, 'yfitall':yvalsall, 'theta-hat':thetamatr, 'theta-cov':thetacov, 'binit':binit, 'window_file':window_file, 'user_sel':user_sel, 'sub_val':x0, 'func':func, 'order':corder, 'chi2dof':chi2dof}  # yfitall will correspond to xspec_interp if input is set.
        # This dictionary is not returned for blackbody fitting.
        # This dictionary does not return chi2, pte, etc...
        #  yfitall will correspond to xin unless iterations are done, then it will correspond to xfitall if xspec_interp is set which is should be.
        #  xtofit, ytofit, yfit, and errtofit should always be same lengths.
        print(fit_dict.keys())
        return fit_dict
           
    # This doesn't have the ability to return_parm for binned window file for polynomial 
    if binit and len(errspec) == 1:  # Need to return thetamatr and covar, this should have return_parm = False
        print('Returned:  xtofit, ytofit, yfit')
        return xtofit, ytofit, yvalsall
    if binit and len(errspec) > 1:
        print('Returned:  xtofit, ytofit, errtofit, yfit')
        return xtofit, ytofit, errtofit, yvalsall        
    if not binit and return_parm == False:  # for spline3, also this is the default for example in lflux() below.
        print('Returned:  yfit for unbinned arrays.')
        return yvalsall
    if not binit and return_parm == True and (func == 'lorentzian' or func == 'gaussian' or func == 'holtsmark'):
        print('Returned yfit and parameters for lorentzian, gaussian, or holtsmark for unbinned arrays.')
        return yvalsall, parm
    if (not binit) and return_parm == True and func == 'poly':
        x0=np.float64(sub_val)
        print('Returned:  yfit, theta-hat, cov-hat, sub_val for unbinned arrays.')
        return yvalsall, thetamatr, thetacov, x0

#  This iterative rejection only works if the original input xpsec = xtofit

def contfit_iter(xspec, yspec,window_file = 'none', user_sel = 'none',  errspec = np.zeros(1), line_file = False, func = 'poly', corder = 1, printvals = False, sel_n = -99.0, binit=False, xspec_interp = np.zeros(1),sub_val=0.0,Tguess=7500.0,return_parm = False, lam0_guess=6562.8, PLOT = False,linetype='abs',gmaguess=1,find_param_sig=0,plot_covariance = False, dT0=3000.0, perturb_dT0=False, LINE_ADJ_WAVE=0.0, nr_cstep=1.0, return_dict = False, n_iter = 2, n_sigrej = 2.5):
# Calls to this should send xspec_interp so that yfitall has same number of elements as this, because fit_dict['xall'] will be shortened after each iteration.
# Example:  ret_dict = SpecLab.contfit_iter(j_arr, Eimg2[w,:], corder=3, n_iter = 3, nsig_rej = 2.5, return_dict= True, xspec_interp = j_arr) 
    
    fit_dict = contfit(xspec, yspec, window_file = window_file, user_sel = user_sel,  errspec = errspec, line_file = line_file, func = func, corder = corder, printvals = printvals, sel_n = sel_n, binit=binit, xspec_interp = xspec_interp,sub_val=sub_val,Tguess=Tguess,return_parm = return_parm, lam0_guess=lam0_guess, PLOT = PLOT,linetype=linetype,gmaguess=gmaguess,find_param_sig=find_param_sig,plot_covariance = plot_covariance, dT0=dT0, perturb_dT0=perturb_dT0, LINE_ADJ_WAVE=LINE_ADJ_WAVE, nr_cstep=nr_cstep, return_dict = return_dict)

    if n_iter > 0:

        n_iter -= 1
        resid = np.array(fit_dict['yfit'] - fit_dict['ytofit'])
        abs_diff = np.abs(resid)
        resid_sig = np.nanstd(resid) 
        noreject = (abs_diff < n_sigrej * resid_sig)
        print(fit_dict['yfit'], fit_dict['ytofit'], fit_dict['func'])
        print('N-iter for rejection = ', n_iter, resid_sig, np.count_nonzero(noreject))
        xspec2 = np.array(fit_dict['xtofit'])
        yspec2 = np.array(fit_dict['ytofit'])
        fit_dict = contfit(xspec2[noreject], yspec2[noreject], window_file = window_file, user_sel = user_sel,  errspec = errspec, line_file = line_file, func = func, corder = corder, printvals = printvals, sel_n = sel_n, binit=binit, xspec_interp = xspec_interp,sub_val=sub_val,Tguess=Tguess,return_parm = return_parm, lam0_guess=lam0_guess, PLOT = PLOT,linetype=linetype,gmaguess=gmaguess,find_param_sig=find_param_sig,plot_covariance = plot_covariance, dT0=dT0, perturb_dT0=perturb_dT0, LINE_ADJ_WAVE=LINE_ADJ_WAVE, nr_cstep=nr_cstep, return_dict = return_dict)
        
    return fit_dict


def lflux(xarr, yarr, lwindow_file = 'linewindows.ecsv', cont_order = -9, c4170 = False, plot_check = True):
    ''' linewidnows.ecsv must have columns:  wid, l1, l2, c1, c2, c3, c4'''
    col_bright = mf.color_bright()
    dat = ascii.read(lwindow_file)
    lineid = np.array(dat['wid'])
    l1 = np.array(dat['l1'])
    c1 = np.array(dat['c1'])
    c2 = np.array(dat['c2'])
    l2 = np.array(dat['l2'])
    c3 = np.array(dat['c3'])
    c4 = np.array(dat['c4'])

    nline = len(c4)
    lineflux = np.zeros(nline)
    equiv_width = np.zeros_like(lineflux)
    yfitcont = np.zeros((nline, len(yarr)))
    c4170flux = np.zeros(nline)
    for n in range(nline):
        
        i1 = findind(xarr, c1[n])
        i4 = findind(xarr, c4[n])
        il1 = findind(xarr, l1[n])
        il2 = findind(xarr, l2[n])
        i2 = findind(xarr, c2[n])
        i3 = findind(xarr, c3[n])
        fullx = xarr[i1:i4+1]
        fully = yarr[i1:i4+1]
        linex = xarr[il1:il2+1]
        liney = yarr[il1:il2+1]

        if c4170:
            c4170flux[n] = np.interp(4170., xarr, yarr)

        if cont_order < 0:  # if continuum is not to be subtracted....these aren't finsihed yet.
            lineflux = np.trapz(liney, x=linex)
            mean_shift = np.trapz(liney * linex, x = linex) / np.trapz(liney, x = linex) # one-sided first central moment
            eff_width = np.trapz(liney, x = linex) / np.max(liney) # SVO filter service
            lfwhm = mf.fwhm(linex, liney, 0.5)
            lpt1m = mf.fwhm(linex, liney, 0.1)
            variance = np.trapz(liney * linex**2, x = linex) / np.trapz(liney, x = linex) # one-sided first central moment
        else:
            yfitcont[n,:] = contfit(xarr, yarr, window_file = lwindow_file, corder = cont_order, line_file = True, sel_n = n)
            lineflux[n] = np.trapz(liney - yfitcont[n,il1:il2+1], x=linex)
            equiv_width[n] = np.trapz( (liney / yfitcont[n,il1:il2+1] - 1.0), x=linex)

            if plot_check:
                f,ax1 = plt.subplots(figsize=(6,4))
                ax1.plot(fullx, fully, color='k',marker='+')
                ax1.plot(xarr,yfitcont[n,:],color=col_bright[3],ls='dashed')
                ax1.plot(linex,liney,color=col_bright[1])
                ax1.plot(linex,liney - yfitcont[n,il1:il2+1],color=col_bright[4])
                ax1.set_ylim(0, np.max(fully))
                ax1.set_xlim(np.min(fullx), np.max(fullx))
                plt.tight_layout()
                plt.savefig('check_'+str(n)+'.pdf')
    line_dict = {'lineid':lineid, 'ew':equiv_width, 'lineflux':lineflux, 'yfitcont':yfitcont,'c4170':c4170flux}
    return line_dict

        
def single_gau( x, c1, mu1, sigma1):
    res =   c1 * np.exp( - (x - mu1)**2.0 / (2.0 * sigma1**2.0) ) 
    return res




def trace_1d(img, yguess = -9, xstrt = -9, otrace=3, bmin=25, bmax=40, tsum=20, ntrace = 50, search_win=10, N_sigrej=4.5, N_iter=3, t_func = 'spline3'):

  #  print('Fitting spline3 to trace')
# Does a trace along spatial direction, only looking at yguess+/-search_win,Also calculates background to subtract
# v3.1: made yguess and xstrt as optional parameters, added flexibility to change order of polynomial and cubic spline option with npieces = otrace

    lenx = len(img[0,:])
    ncol = len(img[0,:])
    nrow = len(img[:,0])
    pix_arr = np.linspace(0,ncol-1, ncol)

    if yguess < 0:
        midx = int(lenx/2)
        test = np.median(img[:,midx-50:midx+50],axis=1)
        yguess = np.argmax(test)
    yguess0 = yguess

    if xstrt < 0:
        xstrt = int(lenx/2)
    
    inc = int(lenx/ntrace)
    yfind = 0.
    yfind_err = 0.
    xx = xstrt
    xfind= 0.

    #while xx < lenx:
    while xx > 0:
       # print(xx)
        test = np.median(img[yguess-search_win:yguess+search_win,xx-int(tsum/2):xx+int(tsum/2)+1],axis=1)  # just search over +/-search_win
        try:
            maxind = np.argmax(test)
        except:
            print('Could not find trace', xx)
            xx = xx - inc
            continue
            

        yl = yguess-search_win
        yu = yguess+search_win
#        yguess_old = yguess
#        yguess_check = maxind + yl  # update yguess to be more accurate for highly curved spectra if there isn't a huge jump

 #       dyguess = np.abs(yguess_check - yguess_old)
 #       if dyguess <=3.5:
        yguess = maxind + yl  # update yguess to be more accurate for highly curved spectra if there isn't a huge jump

       # print('Yguess = ',yguess, xx)

        test = np.median(img[yguess-search_win:yguess+search_win,xx-int(tsum/2):xx+int(tsum/2)+1],axis=1)  # just search over +/-search_win
        
        x = np.arange(0.0,float(len(test)),1.)

        try:
            maxind = np.argmax(test) 
        except:
            print('Could not find trace', xx)
            xx = xx - inc
            continue
        
        try:
            res2 = scipy.optimize.curve_fit( single_gau, x, test, sigma= np.sqrt(np.abs(test)), p0=(np.max(test), float(search_win)/2.0, np.mean(x)),absolute_sigma=True)
            retvals = res2[0]
            covar = res2[1]
            unc_mean = covar[1,1]**0.5 # retvals[2] / np.sqrt( np.abs( np.sum(test) ) )

            if np.abs(retvals[1]) / unc_mean <= 3.0:  ## How well will this deal with non-gaussian spatial profiles like out of focus spetra????
                unc_mean = -99
            
            yfind_err = np.append([yfind_err], unc_mean)
            
            cen = retvals[1] + (yguess - search_win)
            yfind = np.append([yfind], cen)
            xfind = np.append([xfind], xx)
           # print(retvals[1], unc_mean, retvals[2], covar[2,2]**0.5)

           # yguess = int(cen) # update yguess for highly curved spectra
           # print(yguess, cen)
        except:
            cen = float(yguess)
    
        xx = xx - inc

 #   print('Starting over')
    yguess = yguess0
    xx=xstrt+inc
    while xx < lenx:
        test = np.median(img[yguess-search_win:yguess+search_win,xx-int(tsum/2):xx+int(tsum/2)+1],axis=1)  # just search over +/-search_win

        try:
            maxind = np.argmax(test)
        except:
            print('Could not find trace', xx)
            xx = xx + inc
            continue
            
        yl = yguess-search_win
        yu = yguess+search_win

#        yguess_old = yguess
#        yguess_check = maxind + yl  # update yguess to be more accurate for highly curved spectra if there isn't a huge jump 

#        dyguess = np.abs(yguess_check - yguess_old)
#        if dyguess <=3.5:
        yguess = maxind + yl  # update yguess to be more accurate for highly curved spectra if there isn't a huge jump 
      #  print('Yguess = ',yguess, xx, yguess-search_win, yguess+search_win)

        test = np.median(img[yguess-search_win:yguess+search_win,xx-int(tsum/2):xx+int(tsum/2)+1],axis=1)  # just search over +/-search_win
        x = np.arange(0.0,float(len(test)),1.)

        try:
            maxind = np.argmax(test) 
        except:
            print('Could not find trace', xx)
            xx = xx + inc
            continue
            
        try:
            res2 = scipy.optimize.curve_fit( single_gau, x, test, sigma = np.sqrt(np.abs(test)), p0=(np.max(test), float(search_win)/2.0, np.mean(x)),absolute_sigma=True)
            
            retvals = res2[0]
            covar = res2[1]
            unc_mean = covar[1,1]**0.5 # retvals[2]  / np.sqrt( np.abs( np.sum(test) ) )

            if np.abs(retvals[1]) / unc_mean <= 3.0:
                unc_mean = -99
            
            yfind_err = np.append([yfind_err], unc_mean)
            
            cen = retvals[1] + (yguess - search_win)
            yfind = np.append([yfind], cen)
            xfind = np.append([xfind], xx)

        #    print(retvals[1], unc_mean, retvals[2], covar[2,2]**0.5)
            yguess = int(cen) # update yguess for highly curved spectra
           # print(xx, search_win, tsum, yguess, cen)
        except:
            cen = float(yguess)

        xx = xx + inc

    medy = np.median(yfind)
    clean = np.all([yfind > (medy - search_win * 10), yfind < (medy +search_win * 10), yfind_err > -1],axis=0)  # Just get rid of negatives and really really bad fits.
    yvals = yfind[clean]
    xvals = xfind[clean]
    yvals_err = yfind_err[clean]
    args = np.argsort(xvals)
    xvals = xvals[args]
    yvals = yvals[args]
    yvals_err = yvals_err[args]

    if xvals[0] == 0:
        xvals = xvals[1:,]#  Had to exclude first index here because was including pixel = 0 and screwing up the spline3 fitting
        yvals = yvals[1:,]
        yvals_err = yvals_err[1:,]
    
    if t_func == 'spline3':
        global npieces, minW, maxW
       # global xS, yvalS
        xS = xvals  #  Had to exclude first index here because was including pixel = 0 and screwing up the fitting.  
        yvalS = yvals
        yvalS_err = yvals_err
        npieces = otrace
        Carr = np.zeros(npieces + 3)
        minW = np.float64(np.min(pix_arr))
        maxW = np.float64(np.max(pix_arr))

        consts = [npieces, minW, maxW]
        fit = scipy.optimize.curve_fit( spline3n_curvefit, xS, yvalS, sigma=yvalS_err, p0=Carr )
        trace_soln = spline3n(np.float64(pix_arr), fit[0], npieces, minW, maxW)
        trace_soln_course = spline3n(np.float64(xS), fit[0], npieces, minW, maxW)
        # YOU MUST SEND XSPEC_INTERP, here it is pix_arr, FOR SPLINE3 FITTING.  
        #bsub = np.zeros((len(pix_arr)))    

        n_iter = N_iter
        bsub = np.zeros((len(pix_arr)))    
        bb=0 
        while bb < len(pix_arr):
            y1 = int(round(trace_soln[bb] + bmin))
            y2 = int(round(trace_soln[bb] + bmax))
            bpix1 = np.median(img[y1:y2, bb])
            y1 = int(round(trace_soln[bb] - bmin))
            y2 = int(round(trace_soln[bb] - bmax))
            bpix2 = np.median(img[y2:y1, bb])
            bsub[bb] = np.mean([bpix1, bpix2])
            bb=bb+1

        if n_iter == 0:
            return pix_arr, trace_soln, bsub, xS, yvalS
        else:
            nii = 0
            while nii < n_iter:  # iterates with replacement
                #print('Iterating Spline3 fit.')
                resid = trace_soln_course - yvalS
                sdev = np.nanstd(resid)
                cleanX = np.all([ np.abs(resid) < sdev * N_sigrej],axis=0)
                xS_orig = np.zeros_like(xS) + xS
                yvalS_orig = np.zeros_like(yvalS) + yvalS
                yvalS_orig_err = np.zeros_like(yvalS_err) + yvalS_err
                xS = xS[cleanX]
                yvalS = yvalS[cleanX]
                yvalS_err = yvalS_err[cleanX]
                Carr = np.zeros(npieces + 3)
         #       minW = np.float64(np.min(pix_arr))
           #     maxW = np.float64(np.max(pix_arr))
           #     consts = [npieces, minW, maxW]
                fit = scipy.optimize.curve_fit( spline3n_curvefit, xS, yvalS, sigma=yvalS_err, p0=Carr )
                trace_soln = spline3n(np.float64(pix_arr), fit[0], npieces, minW, maxW)
                trace_soln_course = spline3n(np.float64(xS_orig), fit[0], npieces, minW, maxW)
                xS_final = xS
                yvalS_final = yvalS
                yvalS = yvalS_orig
                xS = xS_orig
                yvalS_err = yvalS_orig_err
                nii+=1
            return pix_arr, trace_soln, bsub, xS_final, yvalS_final

                
    yvals_Orig = yvals
    xvals_Orig = xvals
    yvals_err_Orig = yvals_err
    n_iter = N_iter
    soln = np.polyfit(xvals, yvals, otrace, w=1.0/yvals_err) # documentations says this is inverse variance weighting? Hugh?
    if n_iter > 0:
        nii = 0
        while nii < n_iter:  # iterates with replacement
            trace_soln_course = soln[otrace] * xvals_Orig**(otrace-otrace)
            for oo in range(1,int(otrace)+1):
                trace_soln_course += soln[otrace-int(oo)] * xvals_Orig**(int(oo))

            resid = trace_soln_course - yvals_Orig
            sdev = np.std(resid)
            cleanX = np.all([ np.abs(resid) < N_sigrej*sdev],axis=0)
            xvals = xvals_Orig[cleanX]
            yvals = yvals_Orig[cleanX]
            yvals_err = yvals_err_Orig[cleanX]
            soln = np.polyfit(xvals, yvals, otrace, w = 1.0/yvals_err) # documentations says this is inverse variance weighting? Hugh?
            nii+=1

 
    trace_soln_course = soln[otrace] * xvals_Orig**(otrace-otrace)
    for oo in range(1,int(otrace)+1):
        trace_soln_course += soln[otrace-int(oo)] * xvals_Orig**(int(oo))

    trace_soln = soln[otrace] * pix_arr**(otrace-otrace)  # the final solution to the fit:
    for oo in range(1,int(otrace)+1):
        trace_soln += soln[otrace-int(oo)] * pix_arr**(int(oo))

    xvals = xvals_Orig
    yvals = yvals_Orig

    bsub = np.zeros((len(pix_arr)))    
    bb=0 
    while bb < len(pix_arr):
        y1 = int(round(trace_soln[bb] + bmin))
        y2 = int(round(trace_soln[bb] + bmax))
        bpix1 = np.median(img[y1:y2, bb])
        y1 = int(round(trace_soln[bb] - bmin))
        y2 = int(round(trace_soln[bb] - bmax))
        bpix2 = np.median(img[y2:y1, bb])
        bsub[bb] = np.mean([bpix1, bpix2])
        bb=bb+1

    return pix_arr, trace_soln, bsub, xvals, yvals 


def extract_1d_frac(img, pix_arr, trace_soln, bsub, apl = 10, apu = 10, nfrac = 10):
    # taken from imexam4 notebook.
    pp = 0
    ny = len(img[:,0])
    apsumfrac = np.zeros((len(trace_soln)))
    while pp < len(pix_arr)-1:
        col_rebin = rebin(img[:,pp:pp+1], (ny * nfrac, 1))  # nfrac is fractional pixel flux (10 means 0.1 pixel)
        norm_col_rebin = col_rebin * np.sum(img[:,pp:pp+1]) / np.sum(col_rebin)
        trace_10 = int(round(trace_soln[pp]*nfrac))
        apsumfrac[pp] = np.sum(norm_col_rebin[trace_10-int(apl*nfrac):trace_10+int(apu*nfrac)] - \
            bsub[pp]*np.sum(img[:,pp:pp+1]) / np.sum(col_rebin))
        pp = pp + 1
    return apsumfrac


def spline3n_contfit( x,  *params):  # IRAF's spline order 3 n pieces function
    Carr = params
   # Carr = np.zeros((len(params)))
   # Carr = np.zeros(6)
   # Carr[0] = C0
   # Carr[1] = C1
   # Carr[2] = C2
   # Carr[3] = C3
   # Carr[4] = C4
   #Carr[5] = C5
    xmin = MINW   # updated these in v3.
    xmax = MAXW
    s = (x - xmin) / (xmax - xmin) * NPIECES  # xmin and xmax must be over entire range!
    j = np.zeros_like(s)
    kk=0
    while kk < len(j):
        j[kk] = float(int(s[kk]))
        kk = kk + 1
            
    a = (j+1)-s
    b = s-j
    z0 = a**3
    z1 = 1.0 + 3.*a*(1.+a*b)
    z2 = 1.0 + 3.*b*(1.+a*b)
    z3 = b**3
    ii = 0
    y = np.zeros_like(x)
    nn= 4  # for cubic spline
    Zarr = np.zeros((nn, len(x)))
    Zarr[0,:] = z0
    Zarr[1,:] = z1
    Zarr[2,:] = z2
    Zarr[3,:] = z3 
    while ii < nn:
        xx = 0
        while xx < len(x):
            try:
                y[xx] = y[xx] + Zarr[ii,xx]* Carr[ii+int(j[xx])] #* Zarr[ii,xx]
            except:
                # print('failed', ii, j[xx])
                pass
            xx=xx+1
        ii=ii+1
    return y




def spline3n_curvefit( x,  *params):  # IRAF's spline order 3 n pieces function
    Carr = params
   # Carr = np.zeros((len(params)))
   # Carr = np.zeros(6)
   # Carr[0] = C0
   # Carr[1] = C1
   # Carr[2] = C2
   # Carr[3] = C3
   # Carr[4] = C4
   #Carr[5] = C5
    xmin = minW   # updated these in v3.
    xmax = maxW
    s = (x - xmin) / (xmax - xmin) * npieces  # xmin and xmax must be over entire range!
    j = np.zeros_like(s)
    kk=0
    while kk < len(j):
        j[kk] = float(int(s[kk]))
        kk = kk + 1
            
    a = (j+1)-s
    b = s-j
    z0 = a**3
    z1 = 1.0 + 3.*a*(1.+a*b)
    z2 = 1.0 + 3.*b*(1.+a*b)
    z3 = b**3
    ii = 0
    y = np.zeros_like(x)
    nn= 4  # for cubic spline
    Zarr = np.zeros((nn, len(x)))
    Zarr[0,:] = z0
    Zarr[1,:] = z1
    Zarr[2,:] = z2
    Zarr[3,:] = z3 
    while ii < nn:
        xx = 0
        while xx < len(x):
            try:
                y[xx] = y[xx] + Zarr[ii,xx]* Carr[ii+int(j[xx])] #* Zarr[ii,xx]
            except:
                # print('failed', ii, j[xx])
                pass
            xx=xx+1
        ii=ii+1
    return y



def spline3n( x, params, npieces, minW, maxW ):  # IRAF's spline order 3 n pieces function
    Carr = params
   # Carr = np.zeros((len(params)))
   # Carr = np.zeros(6)
   # Carr[0] = C0
   # Carr[1] = C1
   # Carr[2] = C2
   # Carr[3] = C3
   # Carr[4] = C4
   #Carr[5] = C5
    xmin = minW   # updated these in v3.
    xmax = maxW
    s = (x - xmin) / (xmax - xmin) * npieces  # xmin and xmax must be over entire range!
    j = np.zeros_like(s)
    kk=0
    while kk < len(j):
        j[kk] = float(int(s[kk]))
        kk = kk + 1
            
    a = (j+1)-s
    b = s-j
    z0 = a**3
    z1 = 1.0 + 3.*a*(1.+a*b)
    z2 = 1.0 + 3.*b*(1.+a*b)
    z3 = b**3
    ii = 0
    y = np.zeros_like(x)
    nn= 4  # for cubic spline
    Zarr = np.zeros((nn, len(x)))
    Zarr[0,:] = z0
    Zarr[1,:] = z1
    Zarr[2,:] = z2
    Zarr[3,:] = z3 
    while ii < nn:
        xx = 0
        while xx < len(x):
            try:
                y[xx] = y[xx] + Zarr[ii,xx]* Carr[ii+int(j[xx])] #* Zarr[ii,xx]
            except:
                # print('failed', ii, j[xx])
                pass
            xx=xx+1
        ii=ii+1
    return y



#def spline3n_fit2( params, consts):
 #   npieces = consts[0]
 #   minW = consts[1]
 #   maxW = consts[2]
 #   fit = spline3n( x, params , npieces, minW, maxW )
 #   return (fit - yvals)

#def spline3n_fit( params, consts):
 #   npieces = consts[0]
#    minW = consts[1]
  #  maxW = consts[2]
 #   fit = spline3n( xS, params , npieces, minW, maxW )
#    return (fit - yvalS)

#def spline3n_fit( params, npieces ):
#    fit = spline3n( x, params , npieces )
 #   return (fit - yvals)


def convs(win, fin, fwhm):  # same as in syfilter.py
    ''' convs(wave_in, flux_in, FWHM) 
 fwhm in angstroms, disp is dispersion in Ang/pixel, rebins to linear dispersion'''
    disp = win[100]-win[99]
    # rebin to this constant dispersion:
    wlfilt = np.arange(min(win), max(win), disp)
    fin2 = np.interp(wlfilt, win, fin)
    npts = int(10.0 * (fwhm / disp))
    kernel = signal.gaussian(npts, (fwhm / disp)/2.35)
    filtered = signal.convolve(fin2, kernel,mode='same') / sum(kernel)
    return wlfilt, filtered, disp


def get_star(star_name='Sun_FTS_I0'):  # from syfilter.py
    if star_name == 'Sun_FTS_I0':
        try:
            fts = ascii.read('/home/adamkowalski/Dropbox/0-Final_Products/Standard_Spectra/kurucz_fts_flux-reardon/neckel.hamburg.atlas.disk_center_intensity.cgs.ecsv')
            wavein = np.array(fts['wl_ang'])
            fluxin = np.array(fts['ilam_cgs'])
            info = 'From Kevin Reardons collection of atlases.  Converted to erg/s/cm2/sr/Ang at disk center'
        except:
            print('Unable to locate solar spectrum on disk, change directory in SpecLabFunctions.get_star')
    return wavein,fluxin,info
            
def format_coord_qmesh(x, y):
    global X, Y, ZVALS
    xarr=X
    yarr=Y
    colx = mf.findind(xarr,x-0.5)
    rowy = mf.findind(yarr,y-0.5)
    zval = ZVALS[rowy, colx]
    return 'x=%1.4f, y=%1.4f, indx = %1i, indy=%4i, val=%1.4e' % (x, y, colx, rowy, zval)


def qmesh(z,vmin = -9,vmax = -10, cmap='bone'):  # does quick and dirty pcolormesh
    global X, Y, ZVALS
    if vmax < vmin:
        vmax=np.median(z) * 1.5
        vmin=np.median(z) * 0.5
        print(vmax, vmin)
    shp = z.shape
    x = np.arange(0,shp[1],1)
    y = np.arange(0,shp[0],1)

    ZVALS = z
    xx = mf.prep_pmesh(x)
    yy = mf.prep_pmesh(y)
    X = xx
    Y = yy
    xax, yax = np.meshgrid(xx,yy)
    f, ax1=plt.subplots()
    img = ax1.pcolormesh(xax, yax, z, vmax = vmax, vmin = vmin, cmap = cmap,rasterized=True)
    ax1.format_coord = format_coord_qmesh
    cbar = plt.colorbar(img)
    return None

def qmask(z,vmin = -9,vmax = -10, cmap='bone',threshl=0,threshu=6e4,color_thresh='r'):  # does quick and dirty pcolormesh
    global X, Y, ZVALS
    if vmax < vmin:
        vmax=np.median(z) * 1.5
        vmin=np.median(z) * 0.5
        print(vmax, vmin)
    shp = z.shape
    x = np.arange(0,shp[1],1)
    y = np.arange(0,shp[0],1)

    ZVALS = z
    xx = mf.prep_pmesh(x)
    yy = mf.prep_pmesh(y)
    X = xx
    Y = yy
    xax, yax = np.meshgrid(xx,yy)
    xxx, yyy = np.meshgrid(x,y)
    f, ax1=plt.subplots()
    masked_arr = np.ma.masked_where((z > threshl) & (z < threshu),z, copy=True)
    img = ax1.pcolormesh(xax, yax, z, vmax = vmax, vmin = vmin, cmap = cmap,rasterized=True)
    ax1.format_coord = format_coord_qmesh

    plt.scatter(xxx[masked_arr.mask], yyy[masked_arr.mask],marker='+',color=color_thresh)
    cbar = plt.colorbar(img)
    return None




def qplot1(y):
    import matplotlib.pyplot as plt
    f,ax1=plt.subplots()
    x = np.arange(0,len(y),1)
    ax1.plot(x,y,color='black')
    plt.show()
    return None

if __name__ == '__main__':
    import doctest
    doctest.testmod()
