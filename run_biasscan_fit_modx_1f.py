# import ROOT as rt
import bias_scan_fitter as bsf
import optparse
import os

def main(filenames, dates, histonames, files_dates, f1, f2, laydisk, outdir, outfilename, other_pars=None):
	myFitter = bsf.Fitter(filenames, dates, histonames, files_dates, f1, f2, laydisk, outdir, outfilename)
	# myVdepl_dict = myFitter.fitter("%s.root"%outfilename.split('.')[0])
	initpars = other_pars["initpars"]
	pars_limits = other_pars["pars_limits"]
	Vdepl_ref_values = other_pars["Vdepl_ref_values"]
	funcs = other_pars["funcs"]
	is_par_limit = other_pars["is_par_limit"]
	myFitter.add_funcs(funcs)
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
	if is_dates:
		# ------------------------ MOD1 -----------------------------------------
		filenames = ["HVscan_2018.root"] 
		dates = [ # dates when the bias scans were taken
			"2018-08-17 12:00:00", 
			"2018-09-01 12:00:00",
			"2018-09-07 12:00:00", 
			"2018-09-26 12:00:00",
			"2018-10-20 12:00:00"
		] 
		histonames = [] # histogram names (one histo for each date)
		laydisk = "L1"
		# for i in range(25,30):
		# 	histonames.append("AvgNormOnTrkCluCharge_vs_BiasVoltage/HV%s_Lay%s"%(i,laydisk[1]))
		for i in range(14,19):
			histonames.append(
				"AvgNormOnTrkCluCharge_vs_BiasVoltage/HV%s_BmO_SEC2_LYR%s_LDR5_MOD%s" % (i, laydisk[1], 1))
		files_dates = []
		for i in range(0,len(dates)):
			files_dates.append("HVscan_2018.root")
		f1 = [
			[220, 600], 
			[220, 600], 
			[220, 600], 
			[220, 600], 
			[220, 600]
		]
		f2 = [
			[220, 600], 
			[220, 600], 
			[220, 600], 
			[220, 600], 
			[220, 600]
		]
		parentoutdir = '1f_mods'
		outdir = "%s/pdfs_mod1"%parentoutdir
		outtxt = "%s/vdepl_values_mod1.txt"%outdir
		os.system('mkdir %s'%outdir)
		other_pars = {
			"initpars": 
			{
				# "2018-08-17 12:00:00": [20, 250, 50, 0, 0.2],
				# "2018-09-01 12:00:00": [20, 250, 50, 0, 0.2],
				# "2018-09-07 12:00:00": [20, 250, 50, 0, 0.2],
				# "2018-09-26 12:00:00": [20, 250, 50, 0, 0.2],
				# "2018-10-20 12:00:00": [20, 250, 50, 0, 0.2],

				"2018-08-17 12:00:00": [0.05, 250, 100, 1e-3, 0, ],#100, 60],
				"2018-09-01 12:00:00": [0.05, 250, 100, 1e-3, 0, ],#100, 60],
				"2018-09-07 12:00:00": [0.05, 250, 100, 1e-3, 0, ],#100, 60],
				"2018-09-26 12:00:00": [0.05, 250, 100, 1e-3, 0, ],#100, 60],
				"2018-10-20 12:00:00": [0.05, 250, 100, 1e-3, 0, ],#100, 60],
			},
			"pars_limits":
			{
				# "2018-08-17 12:00:00": [[5,35],[220,400],[15,70],[-15,15],[0,1]],
				# "2018-09-01 12:00:00": [[5,35],[220,400],[15,70],[-15,15],[0,1]],
				# "2018-09-07 12:00:00": [[5,35],[220,400],[15,70],[-15,15],[0,1]],
				# "2018-09-26 12:00:00": [[5,35],[220,400],[15,70],[-15,15],[0,1]],
				# "2018-10-20 12:00:00": [[5,35],[220,400],[15,70],[-15,15],[0,1]],

				"2018-08-17 12:00:00": [[10,30], [150,350], [50,150], [0.5e-5,2e-4], [-0.1,0.01], ], #[0.01,0.03], [50,150], [30,90]],
				"2018-09-01 12:00:00": [[10,30], [150,350], [50,150], [0.5e-5,2e-4], [-0.1,0.01], ], #[0.01,0.03], [50,150], [30,90]],
				"2018-09-07 12:00:00": [[10,30], [150,350], [50,150], [0.5e-5,2e-4], [-0.1,0.01], ], #[0.01,0.03], [50,150], [30,90]],
				"2018-09-26 12:00:00": [[10,30], [150,350], [50,150], [0.5e-5,2e-4], [-0.1,0.01], ], #[0.01,0.03], [50,150], [30,90]],
				"2018-10-20 12:00:00": [[10,30], [150,350], [50,150], [0.5e-5,2e-4], [-0.1,0.01], ], #[0.01,0.03], [50,150], [30,90]],
			},
			"is_par_limit":
			{
				"2018-08-17 12:00:00": 5*[False],
				"2018-09-01 12:00:00": 5*[False],
				"2018-09-07 12:00:00": 5*[False],
				"2018-09-26 12:00:00": 5*[False],
				"2018-10-20 12:00:00": 5*[False],
			},
			"Vdepl_ref_values": {
				"2018-08-17 12:00:00":	[428.7565949010766, 61.35170411928435],
				"2018-09-01 12:00:00":	[465.3668049239582, 65.50892013987787],
				"2018-09-07 12:00:00":	[465.6845161989947, 76.49219265766689],
				"2018-09-26 12:00:00":	[434.5431302303973, 71.4604823483927],
				"2018-10-20 12:00:00":	[464.23609443341456, 107.68106565192808]
			},
			"funcs":{
				"2018-08-17 12:00:00": ["3.9766016175 + 0.0462401079049 * x", "19.63412117 + 0.00972167357953 * x"],
				"2018-09-01 12:00:00": ["4.41822856198 + 0.043557466901 * x", "17.5985122582 + 0.0152351122405 * x"],
				"2018-09-07 12:00:00": ["2.55142069994 + 0.0478251056188 * x", "15.8547413786 + 0.0192578670359 * x"],
				"2018-09-26 12:00:00": ["2.60620678658 + 0.0440519856586 * x", "13.9065084027 + 0.0180469683658 * x"],
				"2018-10-20 12:00:00": ["1.30366160411 + 0.0335427102993 * x"," 8.54349806594 + 0.0179475496716 * x"],
			}
		}
		main(filenames, dates, histonames, files_dates, f1, f2, laydisk, outdir, outtxt, other_pars)
		
		# ------------------------ MOD2 -----------------------------------------
		filenames = ["HVscan_2018.root"] 
		dates = [ # dates when the bias scans were taken
			"2018-08-17 12:00:00", 
			"2018-09-01 12:00:00",
			"2018-09-07 12:00:00", 
			"2018-09-26 12:00:00",
			"2018-10-20 12:00:00"
		] 
		histonames = [] # histogram names (one histo for each date)
		laydisk = "L1"
		# for i in range(25,30):
		# 	histonames.append("AvgNormOnTrkCluCharge_vs_BiasVoltage/HV%s_Lay%s"%(i,laydisk[1]))
		for i in range(14,19):
			histonames.append(
				"AvgNormOnTrkCluCharge_vs_BiasVoltage/HV%s_BmO_SEC2_LYR%s_LDR5_MOD%s" % (i, laydisk[1], 2))
		files_dates = []
		for i in range(0,len(dates)):
			files_dates.append("HVscan_2018.root")
		f1 = [
			[260, 600], 
			[260, 600], 
			[300, 600], 
			[280, 600], 
			[340, 600]
		]
		f2 = [
			[260, 600], 
			[260, 600], 
			[300, 600], 
			[280, 600], 
			[340, 600]
		]
		outdir = "%s/pdfs_mod2"%parentoutdir
		outtxt = "%s/vdepl_values_mod2.txt"%outdir
		os.system('mkdir %s'%outdir)
		other_pars = {
			# "initpars": [20, 250, 50, 0, 0.2],
			# "pars_limits":
			# [
			# 	[5,35],
			# 	[220,400],
			# 	[15,70],
			# 	[-15,15],
			# 	[0,1],
			# ],
			"initpars":{
				"2018-08-17 12:00:00": [0.05, 250, 100, 1e-3, 0, ],#100, 60],
				"2018-09-01 12:00:00": [0.05, 250, 100, 1e-3, 0, ],#100, 60],
				"2018-09-07 12:00:00": [0.05, 250, 100, 1e-3, 0, ],#100, 60],
				"2018-09-26 12:00:00": [0.05, 250, 100, 1e-3, 0, ],#100, 60],
				"2018-10-20 12:00:00": [0.05, 250, 100, 1e-3, 0, ],#100, 60],
			},
			"pars_limits":
			{
				"2018-08-17 12:00:00": [[10,30], [150,350], [50,150], [0.5e-5,2e-2], [-0.1,0.01], ], #[0.01,0.03], [50,150], [30,90]],
				"2018-09-01 12:00:00": [[10,30], [150,350], [50,150], [0.5e-5,2e-2], [-0.1,0.01], ], #[0.01,0.03], [50,150], [30,90]],
				"2018-09-07 12:00:00": [[10,30], [150,350], [50,150], [0.5e-5,2e-2], [-0.1,0.01], ], #[0.01,0.03], [50,150], [30,90]],
				"2018-09-26 12:00:00": [[10,30], [150,350], [50,150], [0.5e-5,2e-2], [-0.1,0.01], ], #[0.01,0.03], [50,150], [30,90]],
				"2018-10-20 12:00:00": [[10,30], [150,350], [50,150], [0.5e-5,1e-2], [-2,2], ], #[0.01,0.03], [50,150], [30,90]],
			},
			"is_par_limit":
			{
				"2018-08-17 12:00:00": 5*[True],
				"2018-09-01 12:00:00": 5*[True],
				"2018-09-07 12:00:00": 5*[True],
				"2018-09-26 12:00:00": 5*[True],
				"2018-10-20 12:00:00": 5*[True],
			},
			"Vdepl_ref_values": {
				"2018-08-17 12:00:00":	[397.0110360615524, 41.468545745228425],
				"2018-09-01 12:00:00":	[405.07077064567625, 47.008548595345204],
				"2018-09-07 12:00:00":	[474.36834276085654, 76.46624995721027],
				"2018-09-26 12:00:00":	[424.04272663976116, 50.210556228961494],
				"2018-10-20 12:00:00":	[456.8387218422341, 98.87087166510236],
			},
			"funcs":{
				"2018-08-17 12:00:00": ["0.128209513422 + 0.0363902488383 * x" ,  "11.8023141694 + 0.00698526107832 * x"],
				"2018-09-01 12:00:00": ["0.305756049509 + 0.0354147672397 * x" ,  "10.5808037088 + 0.0100487117159 * x"],
				"2018-09-07 12:00:00": ["0.712291476619 + 0.0336141606004 * x" ,  "14.3910636437 + 0.00477839958078 * x"],
				"2018-09-26 12:00:00": ["0.725258908052 + 0.031363995587 * x" ,  "10.6614646601 + 0.0079319093188 * x"],
				"2018-10-20 12:00:00": ["-0.995455361757 + 0.0283688868045 * x" ,  "6.62537078946 + 0.0116872313606 * x"],
			}	
		}	
		main(filenames, dates, histonames, files_dates, f1, f2, laydisk, outdir, outtxt, other_pars)

		# filenames = ["HVscan_2018.root"] 
		# dates = [ # dates when the bias scans were taken
		# 	"2018-08-17 12:00:00", 
		# 	"2018-09-01 12:00:00",
		# 	"2018-09-07 12:00:00", 
		# 	"2018-09-26 12:00:00",
		# 	"2018-10-20 12:00:00"
		# ] 
		# histonames = [] # histogram names (one histo for each date)
		# laydisk = "L1"
		# # for i in range(25,30):
		# # 	histonames.append("AvgNormOnTrkCluCharge_vs_BiasVoltage/HV%s_Lay%s"%(i,laydisk[1]))
		# for i in range(14,19):
		# 	histonames.append(
		# 		"AvgNormOnTrkCluCharge_vs_BiasVoltage/HV%s_%sOneHVGrp" % (i, laydisk))
		# files_dates = []
		# for i in range(0,len(dates)-5):
		# 	files_dates.append("HVscan_2018.root")
		# f1 = [
		# 	[260, 420], 
		# 	[260, 420], 
		# 	[340, 470], 
		# 	[220, 380], 
		# 	[260, 420]
		# ]
		# f2 = [
		# 	[400, 600], 
		# 	[450, 600], 
		# 	[470, 600], 
		# 	[450, 600], 
		# 	[480, 600]
		# ]
		# outdir = "pdfs_mod3"
		# os.system('mkdir %s'%outdir)
		# main(filenames, dates, histonames, files_dates, f1, f2, laydisk, outdir)

		filenames = ["HVscan_2018.root"] 
		dates = [ # dates when the bias scans were taken
			"2018-08-17 12:00:00", 
			"2018-09-01 12:00:00",
			"2018-09-07 12:00:00", 
			"2018-09-26 12:00:00",
			"2018-10-20 12:00:00"
		] 
		histonames = [] # histogram names (one histo for each date)
		laydisk = "L1"
		# for i in range(25,30):
		# 	histonames.append("AvgNormOnTrkCluCharge_vs_BiasVoltage/HV%s_Lay%s"%(i,laydisk[1]))
		for i in range(14,19):
			histonames.append(
				"AvgNormOnTrkCluCharge_vs_BiasVoltage/HV%s_BmO_SEC2_LYR%s_LDR6_MOD%s" % (i, laydisk[1], 4))
		files_dates = []
		for i in range(0,len(dates)):
			files_dates.append("HVscan_2018.root")
		f1 = [
			[220, 600], 
			[220, 600], 
			[220, 600], 
			[220, 600], 
			[260, 600]
		]
		f2 = [
			[220, 600], 
			[220, 600], 
			[220, 600], 
			[220, 600], 
			[260, 600]
		]
		outdir = "%s/pdfs_mod4"%parentoutdir
		outtxt = "%s/vdepl_values_mod4.txt"%outdir
		os.system('mkdir %s'%outdir)
		other_pars = {
			# "initpars": [20, 250, 50, 0, 0.2],
			# "pars_limits":
			# [
			# 	[5,20],
			# 	[220,400],
			# 	[15,70],
			# 	[-15,15],
			# 	[0,1],
			# ],
			"initpars":{
				"2018-08-17 12:00:00": [10, 250, 100, 1e-3, 0, ],#100, 60],
				"2018-09-01 12:00:00": [10, 250, 100, 1e-3, 0, ],#100, 60],
				"2018-09-07 12:00:00": [10, 250, 100, 1e-3, 0, ],#100, 60],
				"2018-09-26 12:00:00": [10, 250, 100, 1e-3, 0, ],#100, 60],
				"2018-10-20 12:00:00": [10, 250, 100, 1e-3, 0, ],#100, 60],
			},
			"pars_limits":
			{
				"2018-08-17 12:00:00": [[10,20], [150,350], [50,150], [0.5e-5,2e-2], [-15,15], ],#[0.01,0.03], [50,150], [30,90]],
				"2018-09-01 12:00:00": [[10,20], [150,350], [50,150], [0.5e-5,2e-2], [-15,15], ],#[0.01,0.03], [50,150], [30,90]],
				"2018-09-07 12:00:00": [[10,20], [150,350], [50,150], [0.5e-5,2e-2], [-15,15], ],#[0.01,0.03], [50,150], [30,90]],
				"2018-09-26 12:00:00": [[10,20], [150,350], [50,150], [0.5e-5,2e-2], [-15,15], ],#[0.01,0.03], [50,150], [30,90]],
				"2018-10-20 12:00:00": [[10,20], [150,350], [50,150], [0.5e-5,2e-2], [-15,15], ],#[0.01,0.03], [50,150], [30,90]],
			},
			"is_par_limit":
			{
				"2018-08-17 12:00:00": 5*[True],
				"2018-09-01 12:00:00": 5*[True],
				"2018-09-07 12:00:00": 5*[True],
				"2018-09-26 12:00:00": 5*[True],
				"2018-10-20 12:00:00": 5*[True],
			},
			"Vdepl_ref_values":{
				"2018-08-17 12:00:00":	[357.7322919455149, 31.491254878581863],
				"2018-09-01 12:00:00":	[360.2654449710248, 27.697799978204795],
				"2018-09-07 12:00:00":	[361.7456835929801, 42.799164225371925],
				"2018-09-26 12:00:00":	[338.9979463554233, 29.7492642445174],
				"2018-10-20 12:00:00":	[363.0323193240583, 39.32818072402809],
			},
			"funcs":{
				"2018-08-17 12:00:00": ["-3.01949874581 + 0.0673310843759 * x" , "19.6828604549 + 0.00386921718675 * x"],
				"2018-09-01 12:00:00": ["-6.51582923524 + 0.075708508679 * x" , "18.0213431707 + 0.00759991611636 * x"],
				"2018-09-07 12:00:00": ["-9.78810268983 + 0.0816868174922 * x" , "15.46215507 + 0.0118856867393 * x"],
				"2018-09-26 12:00:00": ["-8.40827281099 + 0.0777094467419 * x" , "15.1835620587 + 0.00811659190801 * x"],
				"2018-10-20 12:00:00": ["-11.3199792183 + 0.075463800767 * x" , "10.5236151894 + 0.0152939667193 * x"],
			}
		}
		main(filenames, dates, histonames, files_dates, f1, f2, laydisk, outdir, outtxt, other_pars)
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