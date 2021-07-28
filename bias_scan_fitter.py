import ROOT as rt
import datetime
import math
import collections


def get_intersect(slope1, intersect1, slope2, intersect2, dslope1=0., dintersect1=0., dslope2=0., dintersect2=0.):
    x_intersect = -(intersect2 - intersect1)/(slope2 - slope1)
    try:
        dx_intersect = x_intersect * \
        math.sqrt((dslope1*dslope1 + dslope2*dslope2) / \
                  (slope2-slope1)/(slope2-slope1)+(dintersect1*dintersect1 + dintersect2*dintersect2) / \
                  (intersect2-intersect1)/(intersect2-intersect1))
    except ZeroDivisionError:
        dx_intersect = 0.
    return [x_intersect, dx_intersect]

def tensor_prod_vecs(vec1, vec2):
    if len(vec1) != len(vec2):
        raise ValueError("len(vec1) != len(vec2)")
    tensor = [[] for i in range(len(vec1))]
    for i,el1 in enumerate(vec1):
        for j,el2 in enumerate(vec2):
            tensor[i].append(el1*el2)
    return tensor

def vec_tens_scal_prod(vec, tensor):
    if len(vec) != len(tensor):
        raise ValueError("len(vec) != len(tensor)")
    vector = []
    vec_sum = 0
    for i,_ in enumerate(tensor):
        vec_sum = 0
        for j,_ in enumerate(tensor[i]):
            vec_sum += vec[j]*tensor[j][i]
        vector.append(vec_sum)
    return vector

def antisymm_tens_prod(vec1, vec2):
    return tens_diff(tensor_prod_vecs(vec1,vec2),tensor_prod_vecs(vec2,vec1))

def tens_diff(t1,t2):
    tensor = [[] for i in range(len(t1))]
    for i,_ in enumerate(t1):
        for j,_ in enumerate(t1[i]):
            tensor[i].append(t1[i][j]-t2[i][j])
    return tensor

def vec_scalar_prod(vec1, vec2):
    res = 0
    for i,_ in enumerate(vec1):
        res += vec1[i]*vec2[i]
    return res

class FitFunction(object):
    def __init__(self, tf1):
        self.root_func = tf1
        self.formula = self.root_func.GetExpFormula()
        self._parameters()

    def _parameters(self):
        self.npars = self.root_func.GetNpar()
        self.parnames  = list()
        self.parvalues = list()
        self.parerrors = list()
        for p_i in range(0,self.npars):
            self.parnames.append(self.root_func.GetParName(p_i))
            self.parvalues.append(self.root_func.GetParameter(p_i))
            self.parerrors.append(self.root_func.GetParError(p_i))
    
    def print_pars(self):
        out_str = '%s\n'%self.formula
        out_str +='---------------------------------------------------\n'
        for p_i in range(0, self.npars):
            out_str += '%s: %4.5f +- %4.5f\n'%(self.parnames[p_i], self.parvalues[p_i], self.parerrors[p_i])
        out_str +='===================================================\n'
        return out_str

    def update(self, tf1):
        self.__init__(tf1)
        

class Fitter(object):
    def __init__(self, filenames, dates, histonames, files_dates, f1, f2, laydisk, outdir, outfilenametxt):
        # dates_files = {}
        # files_dates = [""]
        # histonames = [""]
        self.dates = dates
        self.rootfiles = {}
        for i,f in enumerate(filenames):
            self.rootfiles[f] = rt.TFile.Open(f)
        self.dates_hnames={}
        self.histonames = histonames
        for i, d in enumerate(self.dates):
            self.dates_hnames[d] = [
                self.rootfiles[files_dates[i]], histonames[i]]
        self.ths = {}
        self.__f1=f1
        self.__f2=f2
        self.__laydisk = laydisk
        self.outdir = outdir
        self.outfilenametxt = outfilenametxt
        self.vdepl_ref_v = None
        self.funcs = None
        # self.vdepl_ref_e = list()
    
    def add_Vdepl_ref_values_errors(self, Vdepl_ref_values):
        self.vdepl_ref_v = Vdepl_ref_values
    
    def add_funcs(self, funcs):
        self.funcs = funcs
        
    def fitter(self, outname = "fit_test.root"):
        f1 = rt.TF1("f1", "[0]+[1]*x", 0, 600)
        f2 = rt.TF1("f2", "[0]+[1]*x", 0, 600)
        f1_low = rt.TF1("f1_low", "[0]+[1]*x", 0, 600)
        f1_high = rt.TF1("f1_high", "[0]+[1]*x", 0, 600)
        f2_low = rt.TF1("f2_low", "[0]+[1]*x", 0, 600)
        f2_high = rt.TF1("f2_high", "[0]+[1]*x", 0, 600)
        
        f1.SetLineWidth(2)
        f2.SetLineWidth(2)
        f1_low.SetLineStyle(2)
        f1_high.SetLineStyle(2)
        f2_low.SetLineStyle(2)
        f2_high.SetLineStyle(2)

        f_intercept = rt.TLine()
        
        f1_edges = dict(zip(self.dates,self.__f1))
        f2_edges = dict(zip(self.dates,self.__f2))
        print f2_edges
        # print f1_npoints
        # print f2_npoints
        # print self.dates_hnames['2018-10-20 12:00:00'][0]
        # exit()
        ths = self.__histos()
        # print ths
        Vdepl = {}
        Vdepl_err = {}
        # f1_res = 0
        # f2_res = 0
        fout = rt.TFile.Open(outname, "RECREATE")
        fout_vdepl = open(self.outfilenametxt, "w+")
        canv = None
        laydisk = self.__laydisk
        latex = rt.TLatex()
        histo_ymax = 30.
        for d in self.dates:
            f1.SetParameters(0,0.1)
            f2.SetParameters(20,0.01)
            ths[d].SetMarkerStyle(20)
            ths[d].SetMarkerColor(rt.kBlack)
            ths[d].SetLineColor(rt.kBlack)
            ths[d].GetXaxis().SetRangeUser(0,600)
            ths[d].GetYaxis().SetRangeUser(1,histo_ymax)
            print "%s - %s"%(f2_edges[d][0],f2_edges[d][1])
            print "Histo: %s"%ths[d].GetName()
            ths[d].Fit("f1", "", "", f1_edges[d][0], f1_edges[d][1])
            ths[d].Fit("f2", "", "", f2_edges[d][0], f2_edges[d][1])
            ths[d].Fit("f2", "", "", f2_edges[d][0], f2_edges[d][1])
            print ths[d].GetXaxis().GetXmax()
            intersect1 = f1.GetParameter(0)
            intersect2 = f2.GetParameter(0)
            slope1 = f1.GetParameter(1)
            slope2 = f2.GetParameter(1)
            dintersect1 = f1.GetParError(0)
            dintersect2 = f2.GetParError(0)
            dslope1 = f1.GetParError(1)
            dslope2 = f2.GetParError(1)
            f1_low.SetParameters(intersect1-dintersect1, slope1-dslope1)
            f2_low.SetParameters(intersect2-dintersect2, slope2-dslope2)
            f1_high.SetParameters(intersect1+dintersect1, slope1+dslope1)
            f2_high.SetParameters(intersect2+dintersect2, slope2+dslope2)
            ths[d].Write()
            canv = rt.TCanvas("Bias_scan_%s_%s"%(laydisk,d.split(" ")[0].replace("-","_")), "Bias scan, %s, %s"%(laydisk, d), 1000, 800)
            ths[d].SetTitle("Avg. norm. cl. charge, Full scan")
            
            t = canv.GetTopMargin()
            latex.SetNDC()
            latex.SetTextAngle(0)
            latex.SetTextColor(rt.kBlack)
            latex.SetTextFont(51)
            latex.SetTextAlign(31)
            latex.SetTextSize(0.4*t)
            # print str(d)

            ths[d].Draw("E0")
            
            weight = 0
            
            x1_arr = []
            x2_arr = []
            y1_arr = []
            y2_arr = []
            s1_arr = []
            s2_arr = []
            
            for i,val in enumerate(ths[d]):
                if val > 0:
                    # print "%4.2f: %4.4f -> %4.4e : %4.4e" %(ths[d].GetBinCenter(i),val, ths[d].GetBinError(i), ths[d].GetBinError(i)/val)
                    if ths[d].GetBinCenter(i) >= f1_edges[d][0] and ths[d].GetBinCenter(i) <= f1_edges[d][1]:
                        x1_arr.append(ths[d].GetBinCenter(i)/ths[d].GetBinError(i))
                        y1_arr.append(val/ths[d].GetBinError(i))
                        s1_arr.append(1/ths[d].GetBinError(i))
                    elif ths[d].GetBinCenter(i) >= f2_edges[d][0] and ths[d].GetBinCenter(i) <= f2_edges[d][1]:
                        x2_arr.append(ths[d].GetBinCenter(i)/ths[d].GetBinError(i))
                        y2_arr.append(val/ths[d].GetBinError(i))
                        s2_arr.append(1/ths[d].GetBinError(i))
                    # weight += 1/ths[d].GetBinError(i)**2
            print "WEIGHT = %s"%weight

            x_arr = x1_arr
            y_arr = y1_arr
            s_arr = s1_arr
            print x_arr
            print y_arr
            print s_arr

            if len(s_arr) == 0:
                a1=0
                b1=0
            else:
                D1 = vec_scalar_prod(s_arr,s_arr)*vec_scalar_prod(x_arr,x_arr) - (vec_scalar_prod(s_arr,x_arr))**2
                a1 = -vec_scalar_prod(vec_tens_scal_prod(s_arr,antisymm_tens_prod(x_arr,s_arr)),y_arr)/D1
                b1 = -vec_scalar_prod(vec_tens_scal_prod(x_arr,antisymm_tens_prod(s_arr,x_arr)),y_arr)/D1
                print a1

            x_arr = x2_arr
            y_arr = y2_arr
            s_arr = s2_arr

            if len(s_arr) == 0:
                a2=0
                b2=0
            else:
                D2 = vec_scalar_prod(s_arr,s_arr)*vec_scalar_prod(x_arr,x_arr) - (vec_scalar_prod(s_arr,x_arr))**2
                a2 = -vec_scalar_prod(vec_tens_scal_prod(s_arr,antisymm_tens_prod(x_arr,s_arr)),y_arr)/D2
                b2 = -vec_scalar_prod(vec_tens_scal_prod(x_arr,antisymm_tens_prod(s_arr,x_arr)),y_arr)/D2
                print a2

            Vdepl[d] = get_intersect(slope1, intersect1, slope2, intersect2,
                                    dslope1, dintersect1, dslope2, dintersect2)
            
            f_intercept = rt.TLine(Vdepl[d][0], 1, Vdepl[d][0], histo_ymax)
            f_intercept_low = rt.TLine(Vdepl[d][0]-Vdepl[d][1], 1, Vdepl[d][0]-Vdepl[d][1], histo_ymax)
            f_intercept_high = rt.TLine(Vdepl[d][0]+Vdepl[d][1], 1, Vdepl[d][0]+Vdepl[d][1], histo_ymax)
            
            f_intercept.SetLineWidth(2)
            f_intercept_low.SetLineStyle(2)
            f_intercept_high.SetLineStyle(2)

            f1.SetLineColor(rt.kRed)
            f1_low.SetLineColor(rt.kRed+3)
            f1_high.SetLineColor(rt.kRed+3)
            
            f2.SetLineColor(rt.kBlue)
            f2_low.SetLineColor(rt.kBlue+3)
            f2_high.SetLineColor(rt.kBlue+3)

            f_intercept.SetLineColor(rt.kMagenta)
            f_intercept_low.SetLineColor(rt.kMagenta-5)
            f_intercept_high.SetLineColor(rt.kMagenta-5)
            
            f1.Draw("same l")
            f2.Draw("same l")
            f1_low.Draw("same l")
            f1_high.Draw("same l")
            f2_low.Draw("same l")
            f2_high.Draw("same l")
            f_intercept.Draw("same l")
            f_intercept_low.Draw("same l")
            f_intercept_high.Draw("same l")
            latex.DrawLatex(0.4,0.2,d.split(' ')[0])

            rt.gStyle.SetOptStat(0000000)
            canv.Write()
            canv.SaveAs("%s/%s.pdf"%(self.outdir,canv.GetName()))
            fout_vdepl.write("%s\t%s\t-> f1 = %s(%s) + %s(%s) * x (%s) ; f2 = %s(%s) + %s(%s) * x (%s)\n"%(d,Vdepl[d],intersect1,b1,slope1,a1,str(f1_edges[d]),intersect2,b2,slope2,a2,str(f2_edges[d])))
        fout.Write()
        fout_vdepl.close()
        return Vdepl

    def fitter2(self, initpars, pars_limits, is_par_limit, outname = "fit_test.root"):
        f1 = rt.TF1("f1", "[0]/(1+exp(-(x-[1])/[2]))+[3]*x+[4]", 0, 800)
        self.f1 = dict()
        rt.Math.MinimizerOptions.SetDefaultMaxFunctionCalls(100000)
        # self.fit_func = FitFunction(f1)
        # x = ROOT.RooRealVar("x", "x", 0, 10)
        # f1 = rt.TF1("f1", "[0]/(1+exp(-(x-[1])/[2]))+[3]*x+[4]+[5]*exp(-(x-[6])*(x-[6])/2/[7]/[7])", 0, 600)
        f1.SetLineWidth(2)
        f_intercept = rt.TLine()
        f1_edges = dict(zip(self.dates,self.__f1))
        fout = rt.TFile.Open(outname, "RECREATE")
        fout_vdepl = open(self.outfilenametxt, "w+")
        fout_vdepl.write("--------date--------\tVdepl\tError\tZ\t\tV0\talpha\n")
        ths = self.__histos()
        canv = None
        laydisk = self.__laydisk
        latex = rt.TLatex()
        histo_ymax = 30.
        Vdepl = {}
        Vdepl_err = {}
        # f11 = rt.TF1("f11", "[0]+[1]*x", 0, 600)
        # f12 = rt.TF1("f12", "[0]+[1]*x", 0, 600)
        f90p = rt.TF1("f90p", "[0]+[1]*x", 0, 1000)
        f90p_low = rt.TF1("f90p_low", "[0]+[1]*x", 0, 1000)
        f90p_up = rt.TF1("f90p_up", "[0]+[1]*x", 0, 1000)
        # empty_histo = rt.TH1D("empty","empty",1000/ths[d].GetBinWidth(1), 0, 1000)
        # print "self.__getattribute__: "+str(dir(self))
        print ths
        # fout_pars = open('pars.txt',"w+")
        for d in self.dates:
            if self.funcs is not None:
                f11 = rt.TF1("f11", self.funcs[d][0], 0, 600)
                f12 = rt.TF1("f12", self.funcs[d][1], 0, 600)
            for i, p0 in enumerate(initpars[d]):
                f1.SetParameter(i, p0)
            if pars_limits is not None:
                for i, p_limits in enumerate(pars_limits[d]):
                    if is_par_limit[d][i]: f1.SetParLimits(i,p_limits[0],p_limits[1])
            # f1.SetParLimits(1,0,150)
            # f1.SetParLimits(2,0,70)
            # f1.SetParLimits(3,0,8)
            # f1.SetParLimits(4,0,1)
            # f2.SetParameters(20,0.01)

            empty_histo = rt.TH1D("empty","empty",int(1000/ths[d].GetBinWidth(1)), 0, 1000)
            empty_histo.SetName(empty_histo.GetName())
            empty_histo.SetTitle(empty_histo.GetTitle())
            empty_histo.GetXaxis().SetTitle(ths[d].GetXaxis().GetTitle())
            empty_histo.GetYaxis().SetTitle(ths[d].GetYaxis().GetTitle())
            empty_histo.GetXaxis().SetRangeUser(0,600)
            empty_histo.GetYaxis().SetRangeUser(0.0001,ths[d].GetMaximum()*1.1)
            
            ths[d].SetMarkerStyle(20)
            ths[d].SetMarkerColor(rt.kBlack)
            ths[d].SetLineColor(rt.kBlack)
            # ths[d].GetXaxis().SetRangeUser(0,600)
            # ths[d].GetYaxis().SetRangeUser(1,histo_ymax)
            # print "%s - %s"%(f2_edges[d][0],f2_edges[d][1])
            print "Histo: %s"%ths[d].GetName()
            print "DATE: %s"%d
            # ths[d].Scale(1/ths[d].Integral())
            # ths[d].GetYaxis().SetRangeUser(0.0001,0.1)
            ths[d].Fit("f1", "RN0", "", f1_edges[d][0], f1_edges[d][1])
            self.f1[d] = f1.Clone()
            # self.fit_func.update(f1)
            # fout_pars.write(self.fit_func.print_pars())
            # ths[d].Fit("f1", "", "", f1_edges[d][0], f1_edges[d][1])
            # ths[d].Fit("f1", "", "", f1_edges[d][0], f1_edges[d][1])
            ths[d].Write()
            canv = rt.TCanvas("Bias_scan_%s_%s"%(laydisk,d.split(" ")[0].replace("-","_")), "Bias scan, %s, %s"%(laydisk, d), 1000, 800)
            ths[d].SetTitle("Avg. norm. cl. charge, Full scan")
            
            ampl  = f1.GetParameter(0)
            V0    = f1.GetParameter(1)
            alpha = f1.GetParameter(2)
            a     = f1.GetParameter(3)
            b     = f1.GetParameter(4)
            # ampl_gaus = f1.GetParameter(5)
            # mu = f1.GetParameter(6)
            # sigma = f1.GetParameter(7)
            
            dampl  = f1.GetParError(0)
            dV0    = f1.GetParError(1)
            dalpha = f1.GetParError(2)
            da     = f1.GetParError(3)
            db     = f1.GetParError(4)
            
            slope1     = ampl/(4*alpha)
            intersect1 = ampl/2.*(1 - V0/(2*alpha)) + a*V0 + b
            slope2     = a
            intersect2 = ampl + b

            # f11.SetParameters(intersect1, slope1)
            # f12.SetParameters(intersect2, slope2)
            gamma = 0.9
            Z = gamma
            dZ = 0.00
            f90p.SetParameters(gamma*ampl + b, slope2)
            f90p_low.SetParameters((Z-dZ)*ampl + b, slope2)
            f90p_up.SetParameters((Z+dZ)*ampl + b, slope2)


            dslope1     = slope1*math.sqrt((dampl/ampl)**2 + (dalpha/alpha)**2)
            dintersect1 = math.sqrt(
                ((1-V0/(2*alpha))/2.*dampl)**2  +
                (ampl*V0/(4*alpha**2))**2       +
                (V0*da)**2                      +
                db**2
            )
            dslope2     = da
            dintersect2 = math.sqrt(dampl*dampl + db*db)
            
            # Vdepl[d] = get_intersect(slope1, intersect1, slope2, intersect2,
            #                         dslope1, dintersect1, dslope2, dintersect2)
            
            t = canv.GetTopMargin()
            latex.SetNDC()
            latex.SetTextAngle(0)
            latex.SetTextColor(rt.kBlack)
            latex.SetTextFont(51)
            latex.SetTextAlign(31)
            latex.SetTextSize(0.4*t)
            
            empty_histo.Draw()
            ths[d].Draw("E0 same")
            
            f1.Draw("same l")
            if self.funcs is not None:
                f11.SetLineColor(rt.kBlack)
                f11.Draw("same l")
                f12.SetLineColor(rt.kBlack)
                f12.Draw("same l")
            f90p.SetLineColor(rt.kGreen+3)
            f90p_low.SetLineColor(rt.kGreen)
            f90p_low.SetLineStyle(2)
            f90p_up.SetLineColor(rt.kGreen-3)
            f90p_up.SetLineStyle(2)
            f90p.Draw("same l")
            f90p_low.Draw("same l")
            f90p_up.Draw("same l")
            # print (dir(self))
            if self.vdepl_ref_v is not None:
                f_intercept = rt.TLine(self.vdepl_ref_v[d][0], 1, self.vdepl_ref_v[d][0], histo_ymax)
                f_intercept_low = rt.TLine(self.vdepl_ref_v[d][0]-self.vdepl_ref_v[d][1], 1, self.vdepl_ref_v[d][0]-self.vdepl_ref_v[d][1], histo_ymax)
                f_intercept_high = rt.TLine(self.vdepl_ref_v[d][0]+self.vdepl_ref_v[d][1], 1, self.vdepl_ref_v[d][0]+self.vdepl_ref_v[d][1], histo_ymax)
            
                f_intercept.SetLineWidth(2)
                f_intercept_low.SetLineStyle(2)
                f_intercept_high.SetLineStyle(2)
            
                f_intercept.SetLineColor(rt.kMagenta)
                f_intercept_low.SetLineColor(rt.kMagenta-5)
                f_intercept_high.SetLineColor(rt.kMagenta-5)
            
                f_intercept.Draw("same l")
                f_intercept_low.Draw("same l")
                f_intercept_high.Draw("same l")
            
            # vdepl_est = - alpha*math.log((ampl+b)*(1-gamma)/(gamma*ampl+(gamma-1)*b)) + V0
            # Z = gamma - b/ampl*(1-gamma)
            # Z = gamma
            # f1_1 = rt.TF1("f1_1", "[0]/(1+exp(-(x-[1])/[2]))+[3]*x+[4]", 0, 1000)
            # f1_1.SetParameters(ampl, V0, alpha, a, b)
            # f1_2 = rt.TF1("f1_2", "[0]*exp(-(x-[1])*(x-[1])/2/[2]/[2])", 0, 1000)
            # f1_2.SetParameters(ampl_gaus, mu, sigma)
            # f1_1.SetLineColor(rt.kGreen)
            # f1_2.SetLineColor(rt.kBlue)
            # dZ = 0.01
            vdepl_est = - alpha*math.log(1/Z-1) + V0
            vdepl_est_err2 = dV0**2 + (math.log(1/Z-1)*dalpha)**2 + (alpha/(1/Z-1)/Z/Z*dZ)**2
            vdepl_est_err = math.sqrt(vdepl_est_err2)

            f_intercept_curve = rt.TLine(vdepl_est, 0.0001, vdepl_est, empty_histo.GetMaximum())
            f_intercept_curve.SetLineWidth(2)
            f_intercept_curve.SetLineColor(rt.kGreen + 1)
            f_intercept_curve.Draw("same l")
            # f1_1.Draw("same l")
            # f1_2.Draw("same l")
            leg = rt.TLegend(0.65,0.1,0.9,0.3)
            if self.vdepl_ref_v is not None:
                leg.AddEntry(f_intercept, "Vdepl = %4.2f +- %4.2f"%(self.vdepl_ref_v[d][0],self.vdepl_ref_v[d][1]))
            leg.AddEntry(f_intercept_curve, "Vdepl = %4.2f"%vdepl_est)
            if self.vdepl_ref_v is not None:
                leg.AddEntry(f1, "diff = %4.2f"%(vdepl_est-self.vdepl_ref_v[d][0]))
            leg.Draw("same l")
            latex.DrawLatex(0.4,0.2,d.split(' ')[0])
            Vdepl[d] = vdepl_est
            Vdepl_err[d] = vdepl_est_err
            rt.gStyle.SetOptStat(0000000)
            canv.Write()
            canv.SaveAs("%s/%s.pdf"%(self.outdir,canv.GetName()))
            fout_vdepl.write("%s\t%4.2f\t%4.2f\t%4.2f\t%4.2f\t%4.2f\n"%(d, Vdepl[d], Vdepl_err[d], Z, V0, alpha))
        fout.Write()
        fout_vdepl.close()
        return Vdepl
    
    def get_tf1(self, d):
        for i in range(0,4): print self.f1[d].GetParameter(i)
        return self.f1[d]
    def __histos(self):
        ths={}
        dhnms=None
        for d in self.dates:
            dhnms = self.dates_hnames[d][0]
            ths[d] = dhnms.Get(self.dates_hnames[d][1])
            ths[d].GetXaxis().SetRangeUser(0,600)
        # print ths
        # for f in self.rootfiles:
        #     self.rootfiles[f].Close()
        return ths

    def __histos2(self, criteria):
        ths={}
        # dhnms=None
        self.__criteria = criteria
        dhnms = self.dates_hnames[self.dates[0]][0]
        for i,d in enumerate(self.histonames):
            ths[self.__criteria[i]] = dhnms.Get(d)
        # print ths
        # for f in self.rootfiles:
        #     self.rootfiles[f].Close()
        return ths

    def plotter(self, outname):
        colors = [rt.kRed, rt.kMagenta, rt.kBlue, rt.kCyan-3, rt.kGreen+2]
        canv = rt.TCanvas("Bias_%s"%outname.split(".")[0], "Bias_%s"%outname.split(".")[0], 1000, 800)
        canv.Draw()
        ths = self.__histos()
        legend = rt.TLegend(0.1,0.7,0.3,0.9)
        for i,d in enumerate(self.dates):
            ths[d].SetMarkerStyle(24+i)
            ths[d].SetMarkerColor(colors[i])
            ths[d].SetLineColor(colors[i])
            ths[d].GetXaxis().SetRangeUser(0,600)
            ths[d].GetYaxis().SetRangeUser(1,30)
            legend.AddEntry(ths[d], d)
            ths[d].SetFillColor(0)
            # ths[d].Scale(1/ths[d].Integral())
            rt.gStyle.SetOptStat(0000000)
            # ths[d].GetYaxis().SetRangeUser(0,0.12)
            ths[d].Draw("same p")
        legend.Draw("same")
        canv.SaveAs(outname.split('.')[0]+'.pdf')

    def plotter_samedate(self, points, outname):
        colors = [rt.kRed, rt.kMagenta, rt.kBlue, rt.kCyan-3, rt.kGreen+2]
        canv = rt.TCanvas("Bias_%s"%outname.split(".")[0], "Bias_%s"%outname.split(".")[0], 1000, 800)
        canv.Draw()
        ths = self.__histos2(points)
        legend = rt.TLegend(0.1,0.7,0.3,0.9)
        for i,d in enumerate(self.__criteria):
            ths[d].SetMarkerStyle(24+i)
            ths[d].SetMarkerColor(colors[i])
            ths[d].SetLineColor(colors[i])
            ths[d].GetXaxis().SetRangeUser(0,600)
            ths[d].GetYaxis().SetRangeUser(1,30)
            legend.AddEntry(ths[d], d)
            ths[d].SetFillColor(0)
            # ths[d].Scale(1/ths[d].Integral())
            rt.gStyle.SetOptStat(0000000)
            # ths[d].GetYaxis().SetRangeUser(0,0.12)
            ths[d].Draw("same p")
        legend.Draw("same")
        canv.SaveAs(outname.split('.')[0]+'.pdf')