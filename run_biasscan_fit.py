# import ROOT as rt
import bias_scan_fitter as bsf
import optparse

def main(filenames, dates, histonames, files_dates, f1, f2, laydisk, outdir, outfilename, other_pars=None):
	myFitter = bsf.Fitter(filenames, dates, histonames, files_dates, f1, f2, laydisk, outdir, outfilename)
	myVdepl_dict = myFitter.fitter()
	# myVdepl_dict = myFitter.fitter2()
	# print myVdepl_dict
	# for d in dates:
	# 	print "%s: %4.0f +- %4.0f V" % (d, myVdepl_dict[d][0], myVdepl_dict[d][1])

if __name__ == "__main__":
	usage = "usage: %prog [options]"
	parser = optparse.OptionParser(usage)
	parser.add_option("-b", "--batch", 	action="store_true", dest="batch")
	(options, args) = parser.parse_args()
	filenames = [ # names of the files with the cluster charge distributions
		"HVBiasScan_2017_08_14_23_26_BPixonly.root",
		"HVBiasScan_2017_09_23_Lay1BAD_TIMING.root",
		"HVBiasScan_2017_10_04_Lay1only.root",
		"HVBiasScan_2017_10_27_Lay1only.root",
		"HVBiasScan_2017_11_09.root",
		"HVscan_2018.root",
	] 
	dates = [ # dates when the bias scans were taken
		"2017-08-14 12:00:00", 
		"2017-09-23 12:00:00",
		"2017-10-04 12:00:00", 
		"2017-10-27 12:00:00",
		"2017-11-09 12:00:00",

		"2018-05-05 12:00:00", 
		"2018-05-12 12:00:00",
		"2018-05-24 12:00:00", 
		"2018-06-09 12:00:00",
		"2018-07-11 12:00:00", 
		"2018-07-30 12:00:00",
		"2018-08-17 12:00:00", 
		"2018-09-01 12:00:00",
		"2018-09-07 12:00:00", 
		"2018-09-26 12:00:00",
		"2018-10-20 12:00:00"
	] 
	histonames = [] # histogram names (one histo for each date)
	laydisk = "L1"
	for i in range(25,30):
		histonames.append("AvgNormOnTrkCluCharge_vs_BiasVoltage/HV%s_Lay%s"%(i,laydisk[1]))
	for i in range(8,19):
		histonames.append(
			"AvgNormOnTrkCluCharge_vs_BiasVoltage/HV%s_%sOneHVGrp" % (i, laydisk))
	files_dates = [ # files-to-date list files_dates[i] corresponds to dates[i]
		"HVBiasScan_2017_08_14_23_26_BPixonly.root",
		"HVBiasScan_2017_09_23_Lay1BAD_TIMING.root",
		"HVBiasScan_2017_10_04_Lay1only.root",
		"HVBiasScan_2017_10_27_Lay1only.root",
		"HVBiasScan_2017_11_09.root",]
	for i in range(0,len(dates)-5):
		files_dates.append("HVscan_2018.root")
	f1 = [  # ranges of the first fit
			[150, 275],
			[100, 275],
			[100, 275],
			[150, 375],
			[225, 425],

			[150, 220], 
			[140, 260],
			[220, 360], 
			[0,	0], 
			[200, 320], 
			[200, 320], 
			[260, 420], 
			[260, 420], 
			[260, 420], 
			[220, 380], 
			[260, 420]
	]
	f2 = [ # ranges of the second fit
			[275, 425],
			[275, 425],
			[275, 425],
			[375, 505],
			[425, 555],

			[260, 500], 
			[260, 500], 
			[320, 500], 
			[600, 600], 
			[300, 500], 
			[320, 600], 
			[400, 600], 
			[450, 600], 
			[460, 600], 
			[450, 600], 
			[480, 600]
	]
	outdir = "./pdfs_l1_linear"
	outfilename = "./pdfs_l1_linear/vdepl_pars.txt"
	main(filenames, dates, histonames, files_dates, f1, f2, laydisk, outdir, outfilename, other_pars=None)
