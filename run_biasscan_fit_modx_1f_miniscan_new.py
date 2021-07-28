# import ROOT as rt
import bias_scan_fitter as bsf
import optparse
import os

def main(filenames, dates, histonames, files_dates, f1, f2, laydisk, outdir, outfilename, other_pars=None):
	myFitter = bsf.Fitter(filenames, dates, histonames, files_dates, f1, f2, laydisk, outdir, outfilename)
	# myVdepl_dict = myFitter.fitter("%s.root"%outfilename.split('.')[0])
	initpars = other_pars["initpars"]
	pars_limits = other_pars["pars_limits"]
	# pars_limits = None
	is_par_limit = other_pars["is_par_limit"]
	Vdepl_ref_values = other_pars["Vdepl_ref_values"]
	# funcs = other_pars["funcs"]
	# myFitter.add_funcs(funcs)
	myFitter.add_Vdepl_ref_values_errors(Vdepl_ref_values)
	# myVdepl_dict = myFitter.fitter2(initpars, pars_limits)
	myVdepl_dict = myFitter.fitter2(initpars, pars_limits, is_par_limit, "%s.root"%outfilename.split('.')[0])
	# myFitter.plotter(outfilename)
	# myFitter.plotter_samedate(["mod1", "mod2", "mod4"], outfilename)
	# print myVdepl_dict
	# for d in dates:
	# 	print "%s: %4.0f +- %4.0f V" % (d, myVdepl_dict[d][0], myVdepl_dict[d][1])


if __name__ == "__main__":
	usage = "usage: %prog [options]"
	parser = optparse.OptionParser(usage)
	parser.add_option("-b", "--batch", 	action="store_true", dest="batch")
	(options, args) = parser.parse_args()
	is_dates = True
	laydisk = 'L1'
	mods = [1,2,4]
	# mods = [1]
	fout_pars = open('pars.txt',"w+")
	if is_dates:
		for modx in mods:
			filenames = ["HVscan_2018.root"] 
			dates = [
				"2018-08-17 12:00:00", 
				"2018-09-01 12:00:00",
				"2018-09-07 12:00:00", 
				"2018-09-26 12:00:00",
				"2018-10-20 12:00:00"
			]
			histonames = []
			for i in [7,13]: histonames.append("AvgNormOnTrkCluCharge_vs_BiasVoltage/Mod%s_BPixLay1Old_HV%s"%(modx,i))
			files_dates = ["HVscan_2018_apr19.root", "HVscan_2018_jul30.root"]
			f1 = [[0, 600], [220, 600]]
			f2 = [[0, 600], [220, 600]]
			parentoutdir = '1f_mods_mini_scan'
			outdir = "%s/pdfs_mod%s"%(parentoutdir,modx)
			outtxt = "%s/vdepl_values_mod%s.txt"%(outdir,modx)
			os.system('mkdir %s'%outdir)
			other_pars = {
				"initpars": 
				{
					"2018-04-19 12:00:00": [25, 150, 100, 0.01, 0],
					"2018-07-30 12:00:00": [25, 250, 100, 0.01, 0],
				},
				"pars_limits":
				{	
					"2018-04-19 12:00:00": [[10,30], [100,250], [20,150], [0.,0.01], [-5, 10]],
					"2018-07-30 12:00:00": [[16,18], [150,350], [20,80], [0.,0.004], [-5, 10]],
				},
				"is_par_limit":
				{
					"2018-04-19 12:00:00": [False,False,False,False,False],
					"2018-07-30 12:00:00": [True,False,False,True,False],
				},
				"Vdepl_ref_values": {
					"2018-04-19 12:00:00":	[-428.7565949010766, -61.35170411928435],
					"2018-07-30 12:00:00":	[-428.7565949010766, -61.35170411928435],
				},
			# "funcs":{
			# 	"2018-08-17 12:00:00": ["3.9766016175 + 0.0462401079049 * x", "19.63412117 + 0.00972167357953 * x"],
			# 	"2018-09-01 12:00:00": ["4.41822856198 + 0.043557466901 * x", "17.5985122582 + 0.0152351122405 * x"],
			# 	"2018-09-07 12:00:00": ["2.55142069994 + 0.0478251056188 * x", "15.8547413786 + 0.0192578670359 * x"],
			# 	"2018-09-26 12:00:00": ["2.60620678658 + 0.0440519856586 * x", "13.9065084027 + 0.0180469683658 * x"],
			# 	"2018-10-20 12:00:00": ["1.30366160411 + 0.0335427102993 * x"," 8.54349806594 + 0.0179475496716 * x"],
			# }
			}
			myFitter = bsf.Fitter(filenames, dates, histonames, files_dates, f1, f2, laydisk, outdir, outtxt)
			initpars = other_pars["initpars"]
			pars_limits = other_pars["pars_limits"]
			is_par_limit = other_pars["is_par_limit"]
			Vdepl_ref_values = other_pars["Vdepl_ref_values"]
			myFitter.add_Vdepl_ref_values_errors(Vdepl_ref_values)
			myVdepl_dict = myFitter.fitter2(initpars, pars_limits, is_par_limit, "%s.root"%outtxt.split('.')[0])
			mytf1 = None
			for d in dates: 
				mytf1 = myFitter.get_tf1(d)
				fit_func = bsf.FitFunction(mytf1)
				fout_pars.write('%s ||| mod%s ||| '%(d, modx))
				fout_pars.write(fit_func.print_pars())
			# main(filenames, dates, histonames, files_dates, f1, f2, laydisk, outdir, outtxt, other_pars)
		fout_pars.close()
		# main(filenames, dates, histonames, files_dates, f1, f2, laydisk, outdir, outtxt, other_pars)
	else:
		### dates
		f1 = [
			[240, 380], 
			[230, 380], 
			[260, 380], 
			[220, 330], 
			[260, 360]
		]
		f2 = [
			[380, 600], 
			[380, 600], 
			[380, 600], 
			[360, 600], 
			[360, 600]
		]
		dates = [ # dates when the bias scans were taken
			"2018-08-17 12:00:00", 
			"2018-09-01 12:00:00",
			"2018-09-07 12:00:00", 
			"2018-09-26 12:00:00",
			"2018-10-20 12:00:00"
		] 
		
		filenames = ["HVscan_2018.root"] 
		files_dates = []
		ldr_ns = [5,5,6]
		mod_ns = [1,2,4]
		
		for i in range(0,3):
			files_dates.append("HVscan_2018.root")
		
		bias_scan_num = [14,15,16,17,18]
		for n,date in enumerate(dates):
			histonames = [] # histogram names (one histo for each date)
			laydisk = "L1"
			dates1 = [date, date, date]
			# for i in range(25,30):
			# 	histonames.append("AvgNormOnTrkCluCharge_vs_BiasVoltage/HV%s_Lay%s"%(i,laydisk[1]))
			for i,modN in enumerate([1,2,4]):
				histonames.append(
					"AvgNormOnTrkCluCharge_vs_BiasVoltage/HV%s_BmO_SEC2_LYR%s_LDR%s_MOD%s" % (bias_scan_num[n], laydisk[1], ldr_ns[i], modN))
			
			main(filenames, dates1, histonames, files_dates, f1, f2, laydisk, './', "clust_charge_%s.root"%date.split(' ')[0].replace('-','_'))