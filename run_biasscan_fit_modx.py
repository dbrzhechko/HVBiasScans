# import ROOT as rt
import bias_scan_fitter as bsf
import optparse
import os

def main(filenames, dates, histonames, files_dates, f1, f2, laydisk, outdir, outfilename):
	myFitter = bsf.Fitter(filenames, dates, histonames, files_dates, f1, f2, laydisk, outdir, outfilename)
	myVdepl_dict = myFitter.fitter("%s.root"%outfilename.split('.')[0])
	# myVdepl_dict = myFitter.fitter2("%s.root"%outfilename.split('.')[0])
	myFitter.plotter(outfilename)
	# myFitter.plotter_samedate(["mod1", "mod2", "mod4"], outfilename)
	# print myVdepl_dict
	# for d in dates:
	# 	print "%s: %4.0f +- %4.0f V" % (d, myVdepl_dict[d][0], myVdepl_dict[d][1])

if __name__ == "__main__":
	usage = "usage: %prog [options]"
	parser = optparse.OptionParser(usage)
	parser.add_option("-b", "--batch", 	action="store_true", dest="batch")
	(options, args) = parser.parse_args()
	is_dates = not True
	if is_dates:
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
			[300, 420], 
			[300, 460], 
			[340, 470], 
			[300, 460], 
			[330, 480]
		]
		f2 = [
			[480, 600], 
			[480, 600], 
			[470, 600], 
			[460, 600], 
			[480, 600]
		]
		outdir = "pdfs_mod1"
		outtxt = "%s/vdepl_values_mod1.txt"%outdir
		os.system('mkdir %s'%outdir)
		main(filenames, dates, histonames, files_dates, f1, f2, laydisk, outdir, outtxt)
		

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
			[260, 420], 
			[260, 420], 
			[300, 480], 
			[280, 420], 
			[340, 480]
		]
		f2 = [
			[420, 600], 
			[420, 600], 
			[480, 600], 
			[440, 600], 
			[480, 600]
		]
		outdir = "pdfs_mod2"
		outtxt = "%s/vdepl_values_mod2.txt"%outdir
		os.system('mkdir %s'%outdir)
		main(filenames, dates, histonames, files_dates, f1, f2, laydisk, outdir, outtxt)

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
		outdir = "pdfs_mod4"
		outtxt = "%s/vdepl_values_mod4.txt"%outdir
		os.system('mkdir %s'%outdir)
		main(filenames, dates, histonames, files_dates, f1, f2, laydisk, outdir, outtxt)
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