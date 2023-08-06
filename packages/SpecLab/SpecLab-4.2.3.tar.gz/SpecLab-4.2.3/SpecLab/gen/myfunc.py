import numpy as np
import SpecLab.gen.globals as cnst
from scipy.special import gamma, factorial
import matplotlib.pyplot as plt
from astropy.table import Table, Column, MaskedColumn
from astropy.io import ascii
from scipy import interpolate


#def plot_mesh(x,y,z,z0,z1,col,contours=0):
###    if col == 1:
#        ucmap = color_map(umap='rnbw')
#    xx = prep_pmesh(x)
#    yy = prep_pmesh(y)
#    xax, yax = np.meshgrid(xx,yy)

def setplot(fs=16):
    plt.rc('font',size=fs)
    f,ax1=plt.subplots(figsize=(8,6))
    return ax1


def writetwocol(x,y,fname='myfile'):
    dat = Table([x,y],names=['col1','col2'])
    ascii.write(dat,fname+'.ecsv',format='ecsv',overwrite=True)

def writethreecol(x,y,z,fname='myfile'):
    dat = Table([x,y,z],names=['col1','col2','col3'])
    ascii.write(dat,fname+'.ecsv',format='ecsv',overwrite=True)
    

#@njit
def jointgauss2d(xarr,yarr,mux,muy,sigmax,sigmay,rhoxy):
    zsqrd = np.zeros((len(yarr),len(xarr)))
    p = np.zeros_like(zsqrd)
    for x in range(len(xarr)):
        for y in range(len(yarr)):
            zsqrd[y,x] = (xarr[x] - mux)**2/sigmax**2 + (yarr[y]-muy)**2/sigmay**2 - \
                2.0 * rhoxy * (xarr[x] - mux)*(yarr[y] - muy)/sigmax/sigmay
            p[y,x] = 1./(2.0 * np.pi * sigmax * sigmay * np.sqrt(1.0 - rhoxy**2)) * np.exp(-zsqrd[y,x] / (2.0 * (1.0-rhoxy**2)))
    return p
#x = np.arange(0,10,dx)
#y = np.arange(0,10,dy)
# getpdist = jointgauss2d(x,y,mux,muy,sigmax,sigmay,rho)
#xpmesh = mf.prep_pmesh(x)
#ypmesh = mf.prep_pmesh(y)
#xmesh, ymesh = np.meshgrid(x, y)

def gammafn(N):
    t = np.arange(0.001,1e4,0.01)
    t= 10**np.arange(-100,5,0.001)
    yarr = np.exp(-t) * t**(N-1.0)
    return np.trapz(yarr, x=t)
   # return mf.akfactorial(N-1)


def chisqrdist(N, your_Q, reduced = False):
    Q = np.arange(0.01,100,0.01)
    if reduced == True:
        # sub in for Q = Q_reduced * N, then Q above becomes Q_reduced returned by function.
        pdf = 1./gamma(N/2.0)/2.0**(N/2.0) * (N*Q)**(N/2.-1.)*np.exp(-Q*N/2.0) * N
    else: 
        pdf = 1./gamma(N/2.0)/2.0**(N/2.0) * (Q)**(N/2.-1.)*np.exp(-Q/2.0)
    cdf = akcdf(Q, pdf)
    PTE = 1.0-np.interp(your_Q, Q, cdf)
    return Q, pdf, cdf, PTE

def akfactorial(n):
    if n <= 0:
        return 1
    return n * akfactorial(n - 1)

def find_interval(xarr, yarr, conf=.68):
    # returns indices corresponding to confidence interval given by conf, uses twhere a
    # pdf = yarr has equal values and includes 68% of the probability
    dx = xarr[1]-xarr[0]
    cumul = np.cumsum(yarr*dx)
    cumul = akcdf(xarr, yarr, norm=True)
    diff=1.0-conf
    diffp = 10.
    endind = mf.findind(cumul, diff)
    j=0
    while diffp > 0:
        c_end = cumul[j]+conf
        c_ind = mf.findind(cumul, c_end)
        diffp = yarr[c_ind] - yarr[j]
        j=j+1
    return [j-1, c_ind-1]  # indices of xarr

def find_quantile(xarr, yarr, q=.50):
    # q = 0.5 for median, yarr is the PDF, xarr is random variable.
    cumul = akcdf(xarr, yarr, norm=True)
    quantile = np.interp(xarr, yarr, q)
    return quantile

def akcdf(x,y,norm=False):
    ciprime = np.zeros_like(y)
    for j in range(len(x)):
        ciprime[j] = np.trapz(y[0:j],x=x[0:j])

    if norm == True:
        ciprime = ciprime / np.trapz(y, x = x)
    return ciprime


def qplot2(x,y):
    import matplotlib.pyplot as plt
    plt.plot(x,y,color='black')
    plt.show()
    return None

def qplot1(y):
    import matplotlib.pyplot as plt
    f,ax1=plt.subplots()
    x = np.arange(0,len(y),1)
    ax1.plot(x,y,color='black')
    plt.show()
    return None


def gaussrn(xin, ndraw=100, cen=1e4, sig=100, dx=5):
    x = xin
    g = mf.gaussian1(x, mu=cen, sigma=sig)
    g_cdf = mf.akcdf(x, g, norm=True)
    uni = np.random.uniform(size=ndraw)
    ret = np.zeros(len(uni))
    for uu in range(len(uni)):
        ret[uu] = np.interp(uni[uu], g_cdf, x)
    return ret


def gau1_2fit( x, c1, mu1, sigma1):
    res =   c1 * np.exp( - (x - mu1)**2.0 / (2.0 * sigma1**2.0) ) 
    return res

def gaussian1(x = np.zeros(100), mu = 0, sigma = 0, c = -99.0):
    '''  gaussian = gau1(x = np.zeros(100), mu = 0, sigma = 0, c = -99.0)
         if c is negative, it normalizes the gaussian 
 '''
    if sigma == 0:
        print('gau1(x = array, mu = mu, sigma = sigma, c = peak (<0 to return unit normalized, default = -99)')
        return
    if c > 0:
        res =   c * np.exp( - (x - mu)**2.0 / (2.0 * sigma**2.0) )
    if c < 0:
        res =  1./sigma/np.sqrt(2.0 * np.pi) * np.exp( - (x - mu)**2.0 / (2.0 * sigma**2.0) ) # normalized to 1 from -infty to +infty
    return res

def plothist(ydata, dbin = 1.0, gauss = 0,ylog=False, use_standard_estimators=False, retplot=False, xlog=False, xlim=(0,0), ylim=(0,0), retbin = False, shift=True,xlabel='x',ylabel='Number per Bin'):
    # default call to bin2hist is norm=false and dens=false

    # shift should be False if binning integer data, then min of ydata should be center of bin instead of shifting by 0.5 the bin width.
    shp=ydata.shape
    if len(shp) > 1:
        ydata = ydata.flatten()
    # xmin is the MIDDLE of the first bin
    if shift == True:
        xmin = np.min(ydata) + dbin/2.0
    else:
        xmin = np.min(ydata)
    print('Range of data = ',np.min(ydata), ' to', np.max(ydata))
    bins, number_in_bins =  bin2hist(ydata,xmin,dbin)
    import matplotlib.pyplot as plt
    plt.rc('font',size=16)
    f,ax1 = plt.subplots()
    db = bins[1]-bins[0]
    binz = bins - db/2.0
    binz = np.append(binz, binz[-1]+db)
   # ax1.stairs(number_in_bins,binz, color='k')
    ax1.plot(bins, number_in_bins, drawstyle='steps-mid', color='k')
    ax1.plot([binz[0], binz[0]], [0, number_in_bins[0]], color='k')
    ax1.plot([binz[0], bins[0]], [number_in_bins[0], number_in_bins[0]], color='k')
    ax1.plot([binz[-1], binz[-1]], [0, number_in_bins[-1]], color='k')
    ax1.plot([bins[-1], binz[-1]], [number_in_bins[-1], number_in_bins[-1]], color='k')

    if use_standard_estimators:
        m1 = np.mean(ydata)
        m2 = np.std(ydata)
        m3 = np.max(number_in_bins)
    else:
        m1=0
        m2=0
        m3=0
    if ylog == True:
        ax1.set_yscale('log')
    if gauss == 1:
        yfit, params = fit_gauss(bins, number_in_bins,use_standard_estimators=use_standard_estimators,standard_estimators=[m3,m1,m2])  # fit to center of bins
        ax1.plot(bins, yfit, color='#DC050C')
        print('max = {0:.3e}'.format(params[0]),'mean = {0:.3e}'.format(params[1]),'sigma = {0:.3e}'.format(params[2]) )
    if xlog:
        ax1.set_xscale('log')
    if ylog:
        ax1.set_yscale('log')
    if xlim[0] and xlim[1] != 0:
        ax1.set_xlim(xlim)
    if ylim[0] and ylim[1] != 0:
        ax1.set_ylim(ylim)
    ax1.set_xlabel(xlabel)
    ax1.set_ylabel(ylabel)
    plt.tight_layout()
    plt.show()
    if retplot == True or retbin == True:
        return bins, number_in_bins
    else:
        return None
    

def rr(list):
    return np.array(list)


def planckfn(inwave, temp):
    ''' planckfn(wavelength[ang], temp[k])
returns intensity B_lam in units of erg/s/cm2/sr/Angstrom
  can vectorize it along one axis via:
    #  import myfunc as mf
    #  pl = np.vectorize(mf.planckfn)
    #  out = pl(wavearr, singletemperature) '''
    # using my own planck function b/c astropy's keeps changing.
    wl = inwave / 1e8
    Blam = 2.0 * cnst.HPL * (cnst.CC)**2 / (wl)**5 * 1.0 / (np.exp(cnst.CC * cnst.HPL / (wl * cnst.KB * temp)) - 1.0)  * 1e-8  # returns I_lam (intensity per Ang)
    # need to multiply by cnst.PI for flux.
    return Blam # erg/s/cm2/sr/Ang

def planckfni(inwave, temp):
    ''' planckfn(wavelength[ang], temp[k])
returns intensity B_lam in units of erg/s/cm2/sr/Angstrom
  can vectorize it along one axis via:
    #  import myfunc as mf
    #  pl = np.vectorize(mf.planckfn)
    #  out = pl(wavearr, singletemperature) '''
    # using my own planck function b/c astropy's keeps changing.
    wl = inwave / 1e8
    Blam = 2.0 * cnst.HPL * (cnst.CC)**2 / (wl)**5 * 1.0 / (np.exp(cnst.CC * cnst.HPL / (wl * cnst.KB * temp)) - 1.0)  * 1e-8  # returns I_lam (intensity per Ang)
    # need to multiply by cnst.PI for flux.
    return Blam # erg/s/cm2/sr/Ang


def planckfnf(inwave, temp):
    ''' planckfn(wavelength[ang], temp[k])
returns flux B_lam in units of erg/s/cm2/Angstrom
  can vectorize it along one axis via:
    #  import myfunc as mf
    #  pl = np.vectorize(mf.planckfn)
    #  out = pl(wavearr, singletemperature) '''
    # using my own planck function b/c astropy's keeps changing.
    wl = inwave / 1e8
    Blam = np.pi * 2.0 * cnst.HPL * (cnst.CC)**2 / (wl)**5 * 1.0 / (np.exp(cnst.CC * cnst.HPL / (wl * cnst.KB * temp)) - 1.0)  * 1e-8 
    return Blam


def thresh_bitmask_l(arr2d,thresh=0.0):
    ''' mask01, newarr = thresh_bitmask(arr2d, thresh=)'''
    inds= arr2d > thresh
    mask01 = inds.astype(np.int)
    new = arr2d * mask01
    #ax1.pcolormesh(xpmesh,ypmesh,new,cmap='Greys')
    #ax1.scatter(xmesh,ymesh, new, marker='+')
    return mask01, new

def thresh_bitmask_u(arr2d,thresh=0.0):
    ''' mask01, newarr = thresh_bitmask(arr2d, thresh=)'''
    inds= arr2d < thresh
    mask01 = inds.astype(np.int)
    new = arr2d * mask01
    #ax1.pcolormesh(xpmesh,ypmesh,new,cmap='Greys')
    #ax1.scatter(xmesh,ymesh, new, marker='+')
    return mask01, new


def thresh_bitmask_lu(arr2d,threshl=0.0,threshu=6e4):
    ''' mask01, newarr = thresh_bitmask(arr2d, thresh=)'''
    inds= (arr2d > threshl) & (arr2d < threshu)
    mask01 = inds.astype(np.int)
    new = arr2d * mask01
    #ax1.pcolormesh(xpmesh,ypmesh,new,cmap='Greys')
    #ax1.scatter(xmesh,ymesh, new, marker='+')
    return mask01, new


def prep_pmesh(z):
# z is an irregular grid and must be at cell boundaries for pcolormesh (therefore make an array that is ndep + 1 dimensions.)
    ndep = len(z)
    midz = (z[1:len(z)] + z[0:len(z)-1])/2.
    newz = np.insert(midz, 0, z[0] + (z[0]-midz[0]))
    ndep2=len(newz)
    z_bdry = np.append(newz, z[ndep-1] + (z[ndep-1]-midz[ndep-2]))
    return z_bdry


def prep_time(tarr, flarr):
#    from astropy.visualization import time_support
#    time_support()
    import numpy as np
    from astropy.time import Time
#import matplotlib.pyplot as plt
    from astropy.timeseries import TimeSeries
    import astropy.units as u
    import matplotlib.dates as mdates

    nt = len(tarr)
    difft = tarr[1:nt] - tarr[0:nt-1]
    # insert an ordering command.

    tt=np.arange(0,5,1.) + 1.
    ts = TimeSeries(time_start='2016-03-22T12:30:31.32', time_delta=tt * u.s, data={'flux': [1., 3., 4., 2., 4.]})
    fig, ax = plt.subplots()
    ax.plot(Time(ts.time),ts['flux'])
    ax.set_xlim([Time('2016-03-22T12:30:31'), Time('2016-03-22T12:30:38')])
    ax.set_xlabel('UTC on 2016-03-22')
    myFmt = mdates.DateFormatter('%H:%M:%S.%f')
    #myFmt.fmt = myFmt.fmt[:-2]
    plt.gca().xaxis.set_major_formatter(myFmt)
    plt.show()


def binit(tarr, bin_fact):
    ''' binit(array, nbin) where nbin is number of points to bin by '''
    # bin_fact tells the program to average every n pts where n=bin_fact
    nel = len(tarr)
    cutoff = nel % bin_fact
    nel1 = int(nel - cutoff)
    nel2 = int((nel - cutoff)/bin_fact)
    binned_arr = np.zeros(nel2)
    o = 0
    for k in range(nel2):
        binned_arr[k] = np.mean(tarr[o:o+bin_fact])
        o+=bin_fact
    return binned_arr

def bin2hist(indata, bin_start, bin_width, norm=False, dens=False):
    '''bins, number_in_bins =  bin2hist(indata, bin_start,bin_width);  plt.plot(bins, number_in_bins,,marker='+',drawstyle='steps-mid'); default is to return number of occurrences per bin i.e., simple histogram. NOTE:  bin_start is the middle of the first bin'''
    sinds = np.argsort(np.array(indata))
    data = indata[sinds]
    maxdata = np.max(data)
    if bin_start > np.min(indata)+bin_width/2.:
        print('Warning: Min data is =',np.min(indata), ' while lowest bin edge is ', bin_start - bin_width/2.)
    nn = 0
    newcen = bin_start
    while newcen <= np.max(data)+bin_width/2.:
        truth_arr = np.all([data >= (newcen - bin_width/2.), data < (newcen + bin_width/2.)],axis=0)
     #   (data >= (newcen - bin_width/2.) & data < (newcen + bin_width/2.)) # [x,...xn)
        count_true = np.count_nonzero(truth_arr)
        if nn == 0:
            ydata = count_true
            xdata = newcen
        else:
            ydata = np.append(ydata, count_true)
            xdata = np.append(xdata, newcen)
        newcen = bin_start + (nn+1)*bin_width
        nn+=1

    if norm == True and dens == False:
        ydata = ydata / np.sum(ydata)

    if norm == False and dens == True:
        ydata = ydata / bin_width
    arg = np.argmax(ydata)
    print('The mode is ',xdata[arg])
    return xdata, ydata

def fit_gauss(xdata, ydata, use_standard_estimators = False, standard_estimators = (0,0,0)):
    import scipy.optimize
    guess_max = np.max(ydata)
    guess_mean = np.trapz(xdata*ydata, x=xdata) / np.trapz(ydata, x=xdata) # moment
    guess_sig = np.trapz((xdata - guess_mean)**2*ydata, x=xdata) / np.trapz(ydata, x=xdata) # 2nd central moment
    if use_standard_estimators == True:
        guess_max = standard_estimators[0]
        guess_mean = standard_estimators[1]
        guess_sig = standard_estimators[2]
    res = scipy.optimize.curve_fit( gau1_2fit, xdata, ydata, p0=(guess_max, guess_mean, guess_sig))
    
    retvals = res[0]
    best_fit_y = gau1_2fit(xdata, retvals[0], retvals[1], retvals[2])
    print('yfit, [max,mean,sig] = ')
    return best_fit_y, retvals


def fwhm(x,y,fwhm, zero_pt):
    ''' finds a bisector:  fwhm(xarr, yarr, bisec_level, zero_pt) where
           bisec_level is 0.5 returns FWHM'''
    y_baseline = zero_pt
    y_shifted = y - (y.max()-y_baseline) * fwhm
    x_curve = interpolate.UnivariateSpline(x, y_shifted, s=0)
    nroots = len(x_curve.roots())
    roots = x_curve.roots()
    if nroots == 2:
        fwhm = roots[1]-roots[0]
    if nroots > 2:
        maxind = y.argmax()
        vals1 = np.all([roots <= x[maxind]],axis=0)
        vals2 = np.all([roots >= x[maxind]],axis=0)
        fwhm = min(roots[vals2]) - max(roots[vals1])
    return fwhm


def findind(array,value):
    ''' findind(array, value)'''
    idx = (np.abs(array-value)).argmin()
    return idx


def fi(array,value):
    ''' fi(array, value)'''
    idx = (np.abs(array-value)).argmin()
    return idx



# Good color schemes to use from https://www.sron.nl/~pault/
def color_rainbow14(printc = 'no'):
    ''' This is rainbow14 plus grey as last entry, Figure 18 top panel of Paul Tol's website.  color_rainbow(printc = no or yes)'''
    rainbow = [(209,187,215), (174,118,163), (136,46,114), (25,101,176), (82,137,199), (123,175,222), (77,178,101), (144,201,135), (202, 224, 171), (247, 240, 86), (246,193, 65), (241,147,45), (232, 96,28), (220, 5,12), (119, 119, 119)]
    labels=['ltpurple0', 'medpurple1','darkpurple2', 'darkblue3','medblue4', 'lightblue5', 'darkgreen6','medgreen7', 'ltgreen8','yellow9','ltorange10','medorange11', 'dkorange12', 'red13', 'grey14']
    for i in range(len(rainbow)):    
        r, g, b = rainbow[i]    
        rainbow[i] = (r / 255., g / 255., b / 255.)
        if printc == 'yes' or printc =='y':
            print(i, labels[i])
    return rainbow

def color_rainbow23(printc = 'no'):
    ''' This is rainbow23 plus grey as last entry, Figure 18 bottom panel of Paul Tol's website.  color_rainbow(printc = no or yes)'''
    rainbow = [(223,236,251), (217,204,227), (202,172,203), (186,141,180),(170,111,158), (153,79,136),(136,46,114), (25,101,176), (67,125,191), (97,149,207), (123,175,222), (78,178,101),(144,201,135),(202,224,171),(247,240,86), (247,203,69), (244,167,54), (238,128,38),(230,85,24),(220,5,12),(165,23,14),(114,25,14), (66,21,10), (119,119,119) ]
    for i in range(len(rainbow)):    
        r, g, b = rainbow[i]    
        rainbow[i] = (r / 255., g / 255., b / 255.)
    return rainbow

def color_bright(printc='no'):
    ''' color_bright(printc = no or yes) '''
    bright = [(68,119,170), (102,204,238), (34, 136, 51), (204,187,68), (238,102,119), (170,51,119), (187,187,187)]   
    labels=['blue' ,'cyan', 'green', 'yellow','red','purple', 'light grey']
    for i in range(len(bright)):    
        r, g, b = bright[i]    
        bright[i] = (r / 255., g / 255., b / 255.)
        if printc == 'yes' or printc =='y':
            print(i, labels[i])
    return bright

def color_gr():
    greys = [(255./4. * 3., 255./4.*3., 255./4.*3.), (255./4. * 2., 255./4.*2., 255./4.*2. ), (255./4., 255./4., 255./4. )]
    # light to dark grey
    for i in range(len(greys)):    
        r, g, b = greys[i]    
        greys[i] = (r / 255., g / 255., b / 255.)
    print('light to dark greys')
    return greys

def color_map(umap = 'rnbw'):
#    ''' user_cmap = mf.color_map(umap='rnbw') where umap can be burd, burd_flip, or bryl'''
    from matplotlib.colors import LinearSegmentedColormap
    from matplotlib import cm
    if umap == 'rnbw':  # this is rainbow34 aka rainbow_WhBr from Figure 20 of Paul Tol's website for interpolating.
        print('Brown to White rainbow.')
        clrs = ['#E8ECFB', '#DDD8EF', '#D1C1E1', '#C3A8D1', '#B58FC2','#A778B4','#9B62A7', '#8C4E99', '#6F4C9B', '#6059A9',  '#5568B8', '#4E79C5', '#4D8AC6', '#4E96BC', '#549EB3', '#59A5A9', '#60AB9E', '#69B190', '#77B77D', '#8CBC68',  '#A6BE54', '#BEBC48', '#D1B541', '#DDAA3C', '#E49C39', '#E78C35', '#E67932', '#E4632D', '#DF4828', '#DA2222', '#B8221E', '#95211B', '#721E17', '#521A13']
        cmap_name = 'rainbow_brwh'
        usermap = LinearSegmentedColormap.from_list(cmap_name, np.flip(clrs), N=500)
    if umap == 'rnbw_flip':  # this is rainbow34 aka rainbow_WhBr from Figure 20 of Paul Tol's website for interpolating.
        print('Brown to White rainbow.')
        clrs = ['#E8ECFB', '#DDD8EF', '#D1C1E1', '#C3A8D1', '#B58FC2','#A778B4','#9B62A7', '#8C4E99', '#6F4C9B', '#6059A9',  '#5568B8', '#4E79C5', '#4D8AC6', '#4E96BC', '#549EB3', '#59A5A9', '#60AB9E', '#69B190', '#77B77D', '#8CBC68',  '#A6BE54', '#BEBC48', '#D1B541', '#DDAA3C', '#E49C39', '#E78C35', '#E67932', '#E4632D', '#DF4828', '#DA2222', '#B8221E', '#95211B', '#721E17', '#521A13']
        cmap_name = 'rainbow_brwh'
        usermap = LinearSegmentedColormap.from_list(cmap_name, clrs, N=500)
    elif umap == 'burd':
        BuRd = ["#2166AC", "#4393C3", "#92C5DE", "#D1E5F0","#F7F7F7", "#FDDBC7","#F4A582", "#D6604D", "#B2182B"]  # bad = 255,238,153 = FFEE99
        cmap_name = 'BuRd' 
        usermap = LinearSegmentedColormap.from_list(cmap_name, np.flip(BuRd), N=100)
    elif umap == 'burd_flip':
        BuRd = ["#2166AC", "#4393C3", "#92C5DE", "#D1E5F0","#F7F7F7", "#FDDBC7","#F4A582", "#D6604D", "#B2182B"]  # bad = 255,238,153 = FFEE99
        cmap_name = 'BuRd_Flipped' 
        usermap = LinearSegmentedColormap.from_list(cmap_name, BuRd, N=100)
    elif umap == 'bryl':
        clrs_ylbr = ['#FFFFE5', '#FFF7BC','#FEE391','#FEC44F','#FB9A29','#EC7014','#CC4C02', '#993404','#662506']
        cmap_name = 'ylbr'
        usermap = LinearSegmentedColormap.from_list(cmap_name, np.flip(clrs_ylbr), N=500)
    else:
        print( ' umap can be rnbw, burd, burd_flip, or bryl')
        
    return usermap


def format_coord_nearest(x, y):
    ''' define X(meshgrid), Y(meshgrid), xvals, yvals, ZVALS, then use: ax1.format_coord = mf.format_coord_nearest
xax, yax = np.meshgrid(np.linspace(xx1,xx2, 200), np.linspace(yy1,yy2,200))
X = xax
Y = yax
xvals = opt_color
yvals = chi_flare
ZVALS = id_arr
'''
    xarr = X[0,:]
    yarr = Y[:,0]
    flipped=0
    ndep_y = len(yarr)
    if yarr[0] > yarr[ndep_y-1]:
        yarr = np.flip(yarr)
        flipped = 1
    if ((x > xarr.min()) & (x <= xarr.max()) & (y > yarr.min()) & (y <= yarr.max())):
        col = np.searchsorted(xarr, x)-1
        row = np.searchsorted(yarr, y)-1
        if flipped == 1:
            zvals = 'test' #ZVALS[ndep_y-row, col]
        else:
            dist = ((yarr[row] - yvals)**2/(yy2-yy1)**2 + (xarr[col] - xvals)**2/(xx2-xx1)**2)**0.5
            mindist = np.argmin(dist)
            
            zvals = ZVALS[mindist] #ZVALS[row, col]
        return f'x={x:1.4f}, y={y:1.4f}, z={zvals:8s}   [{row},{col}]'
    else:
        return f'x={x:1.4f}, y={y:1.4f}'

