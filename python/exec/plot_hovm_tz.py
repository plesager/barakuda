#
# L. Brodeau, July 2011
#


import sys
import os
import numpy as nmp
from netCDF4 import Dataset

import barakuda_orca as bo
import barakuda_plot as bp
import barakuda_tool as bt



CONFRUN = os.getenv('CONFRUN')
if CONFRUN == None: print 'The CONFRUN environement variable is no set'; sys.exit(0)

DIAG_D = os.getenv('DIAG_D')
if DIAG_D == None: print 'The DIAG_D environement variable is no set'; sys.exit(0)

NN_T = os.getenv('NN_T')
if NN_T == None: print 'The NN_T environement variable is no set'; sys.exit(0)

NN_S = os.getenv('NN_S')
if NN_S == None: print 'The NN_S environement variable is no set'; sys.exit(0)




cname_temp = NN_T
cname_sali = NN_S



#if len(sys.argv) != 4 and len(sys.argv) != 6 :
#    print 'Usage: '+sys.argv[0]+' <YYYY1> <YYYY2> <Nb. Levels> (<name temp.> <name salin.>)'
#    sys.exit(0)

#cy1 = sys.argv[1] ; cy2 = sys.argv[2] ; jy1=int(cy1); jy2=int(cy2)



path_fig=DIAG_D+'/'

fig_type='png'

voceans_u = [cc.upper() for cc in bo.voce2treat]  ; # same list but in uppercase


jo = 0
for coce in bo.voce2treat:



    cf_temp = cname_temp+'_mean_Vprofile_'+CONFRUN+'_'+coce+'.nc' ; bt.chck4f(cf_temp)
    cf_sali = cname_sali+'_mean_Vprofile_'+CONFRUN+'_'+coce+'.nc' ; bt.chck4f(cf_sali)


    id_temp = Dataset(cf_temp)
    if jo == 0:
        vyears = id_temp.variables['time'][:]
        vdepth = id_temp.variables['deptht'][:]
    XT = id_temp.variables[cname_temp][:,:]
    id_temp.close()

    id_sali = Dataset(cf_sali)
    XS = id_sali.variables[cname_sali][:,:]
    id_sali.close()





    if jo == 0:
        vyears = nmp.trunc(vyears) ; # in case 1990.5 => 1990
        jy1=int(min(vyears))
        jy2=int(max(vyears))




    [nby, nz] = XT.shape

    ixtics = bt.iaxe_tick(nby)

    # Number of NaN vertical points:
    visnan = nmp.isnan(XT[0,:])
    nz_nan = nmp.sum(visnan)
    nz = nz - nz_nan


    XTe = nmp.zeros(nby*nz); XTe.shape = [nz, nby]
    XTe[:,:] = nmp.flipud(nmp.rot90(XT[:,:nz]))

    XSe = nmp.zeros(nby*nz); XSe.shape = [nz, nby]
    XSe[:,:] = nmp.flipud(nmp.rot90(XS[:,:nz]))



    # Removing value for first year to all years:
    vy1 = nmp.zeros(nz) ; vy1[:] = XTe[:,0]
    for jy in range(nby): XTe[:,jy] = XTe[:,jy] - vy1[:]
    vy1 = nmp.zeros(nz) ; vy1[:] = XSe[:,0]
    for jy in range(nby): XSe[:,jy] = XSe[:,jy] - vy1[:]


    [ rmin, rmax, rdf ] = bt.get_min_max_df(XTe,40)
    bp.plot_vert_section(vyears[:], vdepth[:nz], XTe[:,:], XTe[:,:]*0.+1., rmin, rmax, rdf,
                         cpal='bbr2', xmin=jy1, xmax=jy2, dx=ixtics, lkcont=False,
                         zmin = vdepth[0], zmax = max(vdepth), l_zlog=True,
                         cfignm=path_fig+'hov_temperature_'+CONFRUN+'_'+coce, cbunit=r'$^{\circ}$C', cxunit='',
                         czunit='Depth (m)',
                         ctitle=CONFRUN+': Spatially-averaged temperature evolution, '+voceans_u[jo]+', ('+str(jy1)+'-'+str(jy2)+')',
                         cfig_type=fig_type, lforce_lim=True, i_sub_samp=2)

    XSe = 1000.*XSe
    [ rmin, rmax, rdf ] = bt.get_min_max_df(XSe,40)
    bp.plot_vert_section(vyears[:], vdepth[:nz], XSe[:,:], XSe[:,:]*0.+1., rmin, rmax, rdf,
                         cpal='bbr2', xmin=jy1, xmax=jy2, dx=ixtics, lkcont=False,
                         zmin = vdepth[0], zmax = max(vdepth), l_zlog=True,
                         cfignm=path_fig+'hov_salinity_'+CONFRUN+'_'+coce, cbunit=r'10$^{-3}$PSU', cxunit='',
                         czunit='Depth (m)',
                         ctitle=CONFRUN+': Spatially-averaged salinity evolution, '+voceans_u[jo]+', ('+str(jy1)+'-'+str(jy2)+')',
                         cfig_type=fig_type, lforce_lim=True, i_sub_samp=2)


    jo = jo +1
