# import ROOT as rt
import bias_scan_fitter as bsf
import optparse

def main(filenames, dates, histonames, files_dates, f1, f2, laydisk, outdir, outfilename,other_pars=None):
	myFitter = bsf.Fitter(filenames, dates, histonames, files_dates, f1, f2, laydisk, outdir, outfilename)
	# myVdepl_dict = myFitter.fitter()
	# f1.SetParameters(20, 100, 50, 0, 0.2)
	# f1.SetParLimits(1,10,30)
	# f1.SetParLimits(1,0,150)
	# f1.SetParLimits(2,0,70)
	# f1.SetParLimits(3,0,8)
	# f1.SetParLimits(4,0,1)
	initpars = other_pars["initpars"]
	# pars_limits = other_pars["pars_limits"]
	pars_limits = None
	myVdepl_dict = myFitter.fitter2(initpars, pars_limits)
	# print myVdepl_dict
	# for d in dates:
	# 	print "%s: %4.0f +- %4.0f V" % (d, myVdepl_dict[d][0], myVdepl_dict[d][1])

if __name__ == "__main__":
	usage = "usage: %prog [options]"
	parser = optparse.OptionParser(usage)
	parser.add_option("-b", "--batch", action="store_true", dest="batch")
	parser.add_option("-o", "--txt-output", action="store", dest="txt_out")
	(options, args) = parser.parse_args()
	filenames = [ # names of the files with the cluster charge distributions
		# "HVBiasScan_2017_08_14_23_26_BPixonly.root",
		# "HVBiasScan_2017_09_23_Lay1BAD_TIMING.root",
		# "HVBiasScan_2017_10_04_Lay1only.root",
		# "HVBiasScan_2017_10_27_Lay1only.root",
		# "HVBiasScan_2017_11_09.root",
		"HVscan_2018.root",
	] 
	dates = [ # dates when the bias scans were taken
		# "2017-08-14 12:00:00", 
		# "2017-09-23 12:00:00",
		# "2017-10-04 12:00:00", 
		# "2017-10-27 12:00:00",
		# "2017-11-09 12:00:00",

		# "2018-05-05 12:00:00", 
		# "2018-05-12 12:00:00",
		# "2018-05-24 12:00:00", 
		# "2018-06-09 12:00:00",
		# "2018-07-11 12:00:00", 
		# "2018-07-30 12:00:00",

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
	# for i in range(8,19):
	# 	histonames.append(
	# 		"AvgNormOnTrkCluCharge_vs_BiasVoltage/HV%s_%sOneHVGrp" % (i, laydisk))
	for i in range(14,19):
		histonames.append(
			"AvgNormOnTrkCluCharge_vs_BiasVoltage/HV%s_%sOneHVGrp" % (i, laydisk))
	files_dates = [ # files-to-date list files_dates[i] corresponds to dates[i]
		# # "HVBiasScan_2017_08_14_23_26_BPixonly.root",
		# # "HVBiasScan_2017_09_23_Lay1BAD_TIMING.root",
		# # "HVBiasScan_2017_10_04_Lay1only.root",
		# # "HVBiasScan_2017_10_27_Lay1only.root",
		# "HVBiasScan_2017_11_09.root",
		]
	for i in range(0,len(dates)):
		files_dates.append("HVscan_2018.root")
	f2 = [ 
			# [0, 600], 
			# [0, 600], 
			# [0, 600], 
			# [0, 600], 
			# [0, 600], 

			# [0, 600],
			# [0, 600],
			# [0, 600],
			# [0, 600],
			# [0, 600], 
			# [0, 600], 
			[0, 600], 
			[0, 600], 
			[0, 600], 
			[0, 600], 
			[0, 600]
	]
	f1 = [ 
			# [0, 600],
			# [0, 600],
			# [0, 600],
			# [0, 600],
			# [0, 600],

			# [0, 600],
			# [0, 600],
			# [0, 600],
			# [0, 600],
			# [0, 600],
			# [0, 600],
			[0, 600], 
			[0, 600], 
			[0, 600], 
			[0, 600], 
			[0, 600]
	]
	# f1 = [ # ranges of the second fit
	# 		[0, 600],
	# 		[0, 600],
	# 		[0, 600],
	# 		[0, 600],
	# 		[0, 600],

	# 		[0, 400], 
	# 		[0, 400], 
	# 		[0, 400], 
	# 		[0, 400], 
	# 		[0, 400], 
	# 		[0, 400], 
	# 		[0, 400], 
	# 		[0, 400], 
	# 		[0, 400], 
	# 		[0, 400], 
	# 		[0, 400]
	# ]
	outdir="pdfs_l1_gaus"
	out_txt_name = options.txt_out
	outfilename="%s/%s"%(outdir, out_txt_name)

	other_pars = {
		"initpars": 
		{
			# "2017-08-14 12:00:00": [20, 250, 50, 0.2, 0],
			# "2017-09-23 12:00:00": [20, 250, 50, 0.2, 0],
			# "2017-10-04 12:00:00": [20, 250, 50, 0.2, 0],
			# "2017-10-27 12:00:00": [20, 250, 50, 0.2, 0],
			# "2017-11-09 12:00:00": [20, 250, 50, 0.2, 0],

			# "2018-05-05 12:00:00": [20, 250, 50, 0.2, 0],
			# "2018-05-12 12:00:00": [20, 250, 50, 0.2, 0],
			# "2018-05-24 12:00:00": [20, 250, 50, 0.2, 0],
			# "2018-06-09 12:00:00": [20, 250, 50, 0.2, 0],
			# "2018-07-11 12:00:00": [20, 250, 50, 0.2, 0],
			# "2018-07-30 12:00:00": [20, 250, 50, 0.2, 0],
			
			# "2018-08-17 12:00:00": [20, 250, 50, 0.2, 0],
			# "2018-09-01 12:00:00": [20, 250, 50, 0.2, 0],
			# "2018-09-07 12:00:00": [20, 250, 50, 0.2, 0],
			# "2018-09-26 12:00:00": [20, 250, 50, 0.2, 0],
			# "2018-10-20 12:00:00": [20, 250, 50, 0.2, 0],

			# "2017-08-14 12:00:00": [0.05, 250, 100, 1e-3, 0, 100, 60],
			# "2017-09-23 12:00:00": [0.05, 250, 100, 1e-3, 0, 100, 60],
			# "2017-10-04 12:00:00": [0.05, 250, 100, 1e-3, 0, 100, 60],
			# "2017-10-27 12:00:00": [0.05, 250, 100, 1e-3, 0, 100, 60],
			# "2017-11-09 12:00:00": [0.05, 250, 100, 1e-3, 0, 100, 60],

			# "2018-05-05 12:00:00": [0.05, 250, 100, 1e-3, 0, 100, 60],
			# "2018-05-12 12:00:00": [0.05, 250, 100, 1e-3, 0, 100, 60],
			# "2018-05-24 12:00:00": [0.05, 250, 100, 1e-3, 0, 100, 60],
			# "2018-06-09 12:00:00": [0.05, 250, 100, 1e-3, 0, 100, 60],
			# "2018-07-11 12:00:00": [0.05, 250, 100, 1e-3, 0, 100, 60],
			# "2018-07-30 12:00:00": [0.05, 250, 100, 1e-3, 0, 100, 60],

			"2018-08-17 12:00:00": [0.05, 250, 100, 1e-3, 0, 100, 60],
			"2018-09-01 12:00:00": [0.05, 250, 100, 1e-3, 0, 100, 60],
			"2018-09-07 12:00:00": [0.05, 250, 100, 1e-3, 0, 100, 60],
			"2018-09-26 12:00:00": [0.05, 250, 100, 1e-3, 0, 100, 60],
			"2018-10-20 12:00:00": [0.05, 250, 100, 1e-3, 0, 100, 60],
		},
		# "pars_limits":
		# {
		# 	# "2017-08-14 12:00:00": [[5,35], [220,400], [15,70], [0,1], [-15,15]],
		# 	# "2017-09-23 12:00:00": [[5,35], [220,400], [15,70], [0,1], [-15,15]],
		# 	# "2017-10-04 12:00:00": [[5,35], [220,400], [15,70], [0,1], [-15,15]],
		# 	# "2017-10-27 12:00:00": [[5,35], [220,400], [15,70], [0,1], [-15,15]],
		# 	# "2017-11-09 12:00:00": [[5,35], [220,400], [15,70], [0,1], [-15,15]],
			
		# 	# "2018-05-05 12:00:00": [[5,35], [220,400], [15,70], [0,1], [-15,15]],
		# 	# "2018-05-12 12:00:00": [[5,35], [220,400], [15,70], [0,1], [-15,15]],
		# 	# "2018-05-24 12:00:00": [[5,35], [220,400], [15,70], [0,1], [-15,15]],
		# 	# "2018-06-09 12:00:00": [[5,35], [220,400], [15,70], [0,1], [-15,15]],
		# 	# "2018-07-11 12:00:00": [[5,35], [220,400], [15,70], [0,1], [-15,15]],
		# 	# "2018-07-30 12:00:00": [[5,35], [220,400], [15,70], [0,1], [-15,15]],

		# 	# "2018-08-17 12:00:00": [[15,35], [220,400], [15,70], [0,1], [-15,15]],
		# 	# "2018-09-01 12:00:00": [[15,35], [220,400], [15,70], [0,1], [-15,15]],
		# 	# "2018-09-07 12:00:00": [[15,35], [220,400], [15,90], [0,1], [-15,15]],
		# 	# "2018-09-26 12:00:00": [[15,35], [220,400], [15,90], [0,1], [-15,15]],
		# 	# "2018-10-20 12:00:00": [[15,35], [220,400], [15,90], [0,1], [-15,15]],

		# 	"2017-08-14 12:00:00": [[0.04,0.09], [150,350], [50,150], [0.5e-5,2e-4], [-0.1,0.01], [0.001,0.03], [50,120], [30,120]],
		# 	"2017-09-23 12:00:00": [[0.04,0.09], [150,350], [50,150], [0.5e-5,2e-4], [-0.1,0.01], [0.001,0.03], [50,120], [30,120]],
		# 	"2017-10-04 12:00:00": [[0.04,0.09], [150,350], [50,150], [0.5e-5,2e-4], [-0.1,0.01], [0.001,0.03], [50,120], [30,120]],
		# 	"2017-10-27 12:00:00": [[0.04,0.09], [150,350], [50,150], [0.5e-5,2e-4], [-0.1,0.01], [0.001,0.03], [50,120], [30,120]],
		# 	"2017-11-09 12:00:00": [[0.04,0.09], [150,350], [50,150], [0.5e-5,2e-4], [-0.1,0.01], [0.001,0.03], [50,120], [30,120]],
						
		# 	"2018-05-05 12:00:00": [[0.04,0.09], [150,350], [50,150], [0.5e-5,2e-4], [-0.1,0.01], [0.001,0.03], [50,120], [30,120]],
		# 	"2018-05-12 12:00:00": [[0.04,0.09], [150,350], [50,150], [0.5e-5,2e-4], [-0.1,0.01], [0.001,0.03], [50,120], [30,120]],
		# 	"2018-05-24 12:00:00": [[0.04,0.09], [150,350], [50,150], [0.5e-5,2e-4], [-0.1,0.01], [0.001,0.03], [50,120], [30,120]],
		# 	"2018-06-09 12:00:00": [[0.04,0.09], [150,350], [50,150], [0.5e-5,2e-4], [-0.1,0.01], [0.001,0.03], [50,120], [30,120]],
		# 	"2018-07-11 12:00:00": [[0.04,0.09], [150,350], [50,150], [0.5e-5,2e-4], [-0.1,0.01], [0.001,0.03], [50,120], [30,120]],
		# 	"2018-07-30 12:00:00": [[0.04,0.09], [150,350], [50,150], [0.5e-5,2e-4], [-0.1,0.01], [0.001,0.03], [50,120], [30,120]],

		# 	"2018-08-17 12:00:00": [[0.04,0.09], [150,350], [50,150], [0.5e-5,2e-4], [-0.1,0.01], [0.001,0.03], [50,120], [30,120]],
		# 	"2018-09-01 12:00:00": [[0.04,0.09], [150,350], [50,150], [0.5e-5,2e-4], [-0.1,0.01], [0.001,0.03], [50,180], [30,120]],
		# 	"2018-09-07 12:00:00": [[0.04,0.12], [150,350], [50,150], [0.5e-5,2e-4], [-0.1,0.01], [0.001,0.02], [50,180], [30,150]],
		# 	"2018-09-26 12:00:00": [[0.04,0.09], [150,350], [50,150], [0.5e-5,2e-4], [-0.1,0.01], [0.001,0.03], [50,180], [30,120]],
		# 	"2018-10-20 12:00:00": [[0.04,0.09], [150,350], [50,150], [0.5e-5,2e-4], [-0.1,0.01], [0.001,0.03], [50,180], [30,120]],
		# },
	}
	main(filenames, dates, histonames, files_dates, f1, f2, laydisk, outdir, outfilename, other_pars)
