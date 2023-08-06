# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
# Copyright (C) 2015-2018 GEM Foundation
#
# OpenQuake is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# OpenQuake is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with OpenQuake. If not, see <http://www.gnu.org/licenses/>.

"""
Module exports :class:`ChaoEtAl2020SInter`
               :class:`ChaoEtAl2020SSlab`
               :class:`ChaoEtAl2020Asc`
"""
import math

import numpy as np

from openquake.baselib.general import CallableDict
from openquake.hazardlib import const
from openquake.hazardlib.gsim.base import GMPE, CoeffsTable
from openquake.hazardlib.imt import PGA, PGD, PGV, SA

CONSTANTS = {'mag_ref': 6.5, 'n': 2, 'vs30_ref': 760, 'rrup_ref': 0}


def _fc(C, imt, vs30, sa1180):
    """
    C value factor [23].
    """
    s = CONSTANTS
    if imt.string in ["PGD", "PGV"]:
        c = 2400
    else:
        c = 2.4

    return (-1.5 * np.log(vs30 / s['vs30_ref']) - np.log(sa1180 + c)
            + np.log(sa1180 + c * (vs30 / s['vs30_ref']) ** 1.5)) \
        * np.heaviside(s['vs30_ref'] - vs30, 0.5) * C['c23']


_ffault = CallableDict()


@_ffault.add(const.TRT.SUBDUCTION_INTERFACE, const.TRT.SUBDUCTION_INTRASLAB)
def _ffault_1(trt, MC, SUFFIX, C, mag):
    """
    Other fault specific factors.
    """
    return (6 - mag) * np.heaviside(6 - mag, 0.5) * C['c13'] \
        + (mag - MC) * np.heaviside(mag - MC, 0.5) \
        * C['c29' + SUFFIX]


@_ffault.add(const.TRT.ACTIVE_SHALLOW_CRUST)
def _ffault_2(trt, MC, SUFFIX, C, mag):
    """
    Other fault specific factors.
    """
    return ((mag - CONSTANTS['mag_ref']) ** 2 - (mag - MC) ** 2
            * np.heaviside(mag - MC, 0.5)) * C['c10']


def _fh(trt, SBCR, MC, C4, C, mag, rrup):
    """
    Factors using `h` (coefficients 17-22).
    """
    s = CONSTANTS
    if trt == const.TRT.SUBDUCTION_INTERFACE:
        # H factor for coefficients 17-22
        h = 10 * np.exp(C4 * (mag - MC) * np.heaviside(mag - MC, 0.5))
    else:  # ASC
        h = 10.
    hf = np.log((rrup ** s['n'] + h ** s['n']) ** (1 / s['n'])
                / (s['rrup_ref'] ** s['n'] + h ** s['n']) ** (1 / s['n']))

    if trt == const.TRT.ACTIVE_SHALLOW_CRUST:
        c19 = mag
    else:
        c19 = np.minimum(mag, MC)
    return hf * C['c17' + SBCR] + hf * C['c19' + SBCR] * (c19 - s['mag_ref'])


_ftype = CallableDict()


@_ftype.add(const.TRT.SUBDUCTION_INTERFACE, const.TRT.SUBDUCTION_INTRASLAB)
def _ftype_1(trt, suffix, C, ctx):
    """
    Factor based on the type of fault.
    """
    return C['c4' + suffix]


@_ftype.add(const.TRT.ACTIVE_SHALLOW_CRUST)
def _ftype_2(trt, suffix, C, ctx):
    """
    Factor based on the type of fault.
    """
    res = np.full_like(ctx.rake, C['c2'])  # strike-slip
    res[(30 <= ctx.rake) & (ctx.rake <= 150)] = C['c1']  # reverse
    res[(-150 <= ctx.rake) & (ctx.rake <= -30)] = C['c3']  # normal
    return res


def _fvs30(geology, C, ctx):
    """
    Source of Vs30 factor.
    vs30measured available for Kuo17 (measured)
    self.geology True for KS17 (inferred)
    self.geology False for Receiver Function (inferred)
    """
    return np.where(ctx.vs30measured, C['c26'],
                    C['c27'] if geology else C['c28'])


def _fz1pt0(C, ctx):
    """
    z1pt0 factor.
    """
    result = np.zeros_like(ctx.z1pt0)
    idx = ctx.z1pt0 >= 0
    if sum(idx) == 0:
        return result

    z1pt0_ref = np.exp(-4.08 / 2 * np.log((ctx.vs30 ** 2 + 355.4 ** 2)
                                          / (1750 ** 2 + 355.4 ** 2)))
    result[idx] = np.log(ctx.z1pt0[idx] / z1pt0_ref) * C['c25']
    return result


def get_stddevs(f, C, mag):
    """
    Standard deviation.
    tau: between event stddev ln(g)
    phis2s: between site stddev in ln(g)
    phiss: single station stddev in ln(g)
    """
    f_mag = 0.5 * (np.minimum(6.5, np.maximum(4.5, mag)) - 4.5)
    tau = C[f'tau1{f}'] + (C[f'tau2{f}'] - C[f'tau1{f}']) * f_mag
    phiss = C[f'phiss1{f}'] + (C[f'phiss2{f}'] - C[f'phiss1{f}']) * f_mag
    phis2s = C['phis2s']
    phi = np.sqrt(phis2s ** 2 + phiss ** 2)
    return [np.sqrt(tau ** 2 + phi ** 2), tau, phi]


class ChaoEtAl2020SInter(GMPE):
    """
    Chao et al. (2020) for Subduction Interface.
    """

    DEFINED_FOR_TECTONIC_REGION_TYPE = const.TRT.SUBDUCTION_INTERFACE

    DEFINED_FOR_INTENSITY_MEASURE_COMPONENT = const.IMC.GEOMETRIC_MEAN

    DEFINED_FOR_INTENSITY_MEASURE_TYPES = {PGA, PGD, PGV, SA}

    DEFINED_FOR_REFERENCE_VELOCITY = 1180

    DEFINED_FOR_STANDARD_DEVIATION_TYPES = {
        const.StdDev.TOTAL, const.StdDev.INTER_EVENT, const.StdDev.INTRA_EVENT}

    #: Required distance rrup
    REQUIRES_DISTANCES = {'rrup'}

    REQUIRES_RUPTURE_PARAMETERS = {'mag', 'ztor'}

    REQUIRES_SITES_PARAMETERS = {'vs30', 'vs30measured', 'z1pt0'}

    REQUIRES_ATTRIBUTES = {'manila', 'aftershocks', 'geology'}

    def __init__(self, manila=False, aftershocks=False, geology=True,
                 **kwargs):
        """
        Aditional parameters.
        """
        super().__init__(manila=manila, aftershocks=aftershocks,
                         geology=geology, **kwargs)
        # Manila or Ryukyu subduction zone
        self.manila = manila
        # aftershocks or mainshocks
        self.aftershocks = aftershocks
        # geology True for KS17, False for seismic (receiver function)
        # only used for inferred vs30, otherwise use vs30measured
        self.geology = geology

    def compute(self, ctx: np.recarray, imts, mean, sig, tau, phi):
        """
        See :meth:`superclass method
        <.base.GroundShakingIntensityModel.compute>`
        for spec of input and result values.
        """
        trt = self.DEFINED_FOR_TECTONIC_REGION_TYPE
        for m, imt in enumerate(imts):
            C = self.COEFFS[imt]

            s = CONSTANTS
            med = mean[m]

            med += _ftype(trt, self.SUFFIX, C, ctx)
            med += (ctx.ztor - self.CONST_FAULT['href']) * C[
                'c14' + self.SUFFIX]
            med += (ctx.mag - s['mag_ref']) * C['c8' + self.SBCR]
            med += (5 - ctx.mag) * np.heaviside(5 - ctx.mag, 0.5) \
                * C['c11' + self.SBCR]
            med += _fh(trt, self.SBCR, self.MC, self.CONST_FAULT['C4'],
                       C, ctx.mag, ctx.rrup)

            med += (ctx.rrup - s['rrup_ref']) * C['c21' + self.SBCR]
            med += _ffault(trt, self.MC, self.SUFFIX, C, ctx.mag)
            med += C['c6'] * self.aftershocks + C['c7'] * self.manila
            med += _fvs30(self.geology, C, ctx)

            sa1180 = np.exp(med + math.log(1180/s['vs30_ref']) * C['c24'])
            med += _fc(C, imt, ctx.vs30, sa1180)
            med += np.log(ctx.vs30 / s['vs30_ref']) * C['c24']
            med += _fz1pt0(C, ctx)

            sig[m], tau[m], phi[m] = get_stddevs(self.SBCR, C, ctx.mag)

    COEFFS = CoeffsTable(sa_damping=5, table="""\
    imt    c1                  c2                  c3                  c4_if               c4_is               c6                  c7                 c8_cr              c8_sb               c10                 c11_cr              c11_sb              c13                 c14_cr              c14_if              c14_is              c17_cr              c17_sb             c19_cr             c19_sb              c21_cr              c21_sb              c23                 c24                c25                 c26                 c27                 c28                 c29_if              c29_is             tau1_cr            tau2_cr            tau1_sb            tau2_sb            phiss1_cr          phiss2_cr          phiss1_sb          phiss2_sb          phis2s
    pga   -0.5192892547128840 -0.6150055029113330 -0.6487900726643910 -0.5859618870941580  0.2995078226527580 -0.1252895878217900  0.1860213693406720 0.4128529204313240 0.6654099729223670 -0.1376176044286790 -0.0000003768045793 -0.0000002632651801 -0.0000003479033210  0.0325013808122898  0.0188003326071965  0.0066214814780273 -1.3033352051553600 -1.4222150700864700 0.3874353293578060 0.1816390684494260 -0.0034295741595448 -0.0034489780547407 -2.5525572055834000 -0.4820755783830470 0.0636111092153052 -0.5680621936097360 -0.6441908224323110 -0.6148407238174470 -0.4944663117848010 -0.4948250053327020 0.3674988948492440 0.3156766103555770 0.2747114934261350 0.5404436414423900 0.5284243730959070 0.4400249261948010 0.4358918335042310 0.4982604989025690 0.3435860891378130
    0.01  -0.5185435292277630 -0.6139978370809050 -0.6485291075803880 -0.5838899830711630  0.3025167286045810 -0.1244749736423930  0.1818440946548220 0.4133627969553290 0.6662082185566420 -0.1377874122648280 -0.0000016455914614 -0.0000010168484829 -0.0000015396189431  0.0325478379384533  0.0187424764459864  0.0065978989650052 -1.3050707375477800 -1.4244518028964800 0.3865358127626830 0.1799727376957520 -0.0034138067537784 -0.0034249196892139 -2.5491215932210800 -0.4817847143782920 0.0637979244436324 -0.5671019863928200 -0.6430624549208040 -0.6134855454872920 -0.4962061562087430 -0.5019638690208290 0.3672959719907850 0.3154146574183840 0.2733100640145130 0.5413688232186000 0.5279530156395120 0.4402345932395540 0.4366852410606870 0.4979773327789170 0.3437466383316600
    0.02  -0.4925935193382860 -0.5849494939894080 -0.6149768931486030 -0.5994558769715950  0.2896423927820520 -0.1255022048822760  0.1913815871815020 0.3989282252665750 0.6316076153041100 -0.1329759746961010 -0.0010277552092071 -0.0000007415198554 -0.0000009243529219  0.0330191056515263  0.0184348278192339  0.0069331416349393 -1.3381199569179700 -1.4144452691294700 0.3918303510961290 0.1909212976216070 -0.0031761225955272 -0.0036500842576487 -2.5020049297189400 -0.4722757215196650 0.0649888427251637 -0.5300330753401030 -0.6092543141804070 -0.5783932279622350 -0.4567832202723850 -0.4843335992997120 0.3672096025203770 0.3193604175283950 0.2727371846461310 0.5590662841638730 0.5212490565944880 0.4457229793375830 0.4284446929672800 0.4997055429236690 0.3492753254041860
    0.03  -0.4773436137435830 -0.5646500549184690 -0.5823569579995780 -0.6229871080555090  0.2895352598530250 -0.1281741601414120  0.1959394907475940 0.3700049726661150 0.5722615232020440 -0.1233348788754380 -0.0013400986538279 -0.0000008780800013 -0.0000010741358947  0.0343101384872960  0.0183116904998815  0.0075119701817267 -1.3673880371344400 -1.4049670408467200 0.4087284138519370 0.2120199290459480 -0.0031597614295051 -0.0039690305196895 -2.3679999172581600 -0.4533571902303470 0.0688570330004100 -0.4674371210038970 -0.5547847971008720 -0.5162080030607480 -0.3909967282502120 -0.4568941706767360 0.3659401986651120 0.3269487169641220 0.2754713073378610 0.5782229669599770 0.5138814813317350 0.4562412368820710 0.4231963576524820 0.5062146219159800 0.3642070292163550
    0.05  -0.4384226473479580 -0.5082028496350560 -0.4996495791530560 -0.5509927916841400  0.4201424505033270 -0.1278113776092280  0.2242032272922090 0.3277716179853340 0.5335838412677030 -0.1092566090939630 -0.0009524028343619 -0.0000009362783788 -0.0000012076824503  0.0374313441023976  0.0179647463512188  0.0086002417698971 -1.4043378692826500 -1.4529353769070100 0.4227955124257500 0.2059482358996180 -0.0037038172429266 -0.0042767503271602 -2.0984569938797400 -0.4174769587709540 0.0796477449779514 -0.3278239226800660 -0.4273786543769590 -0.3669057022159870 -0.3673342531461080 -0.4926026405594960 0.3613130559351250 0.3457148557860690 0.2827051741664680 0.6026422039770350 0.5030028370059200 0.4708951658491060 0.4104373460235670 0.5195083771826150 0.4080959377619060
    0.075 -0.3477680472987080 -0.3945396148772630 -0.3644851574401720 -0.3788975825498850  0.6660790354369400 -0.1257199250776420  0.2590114609066670 0.3280509470422620 0.5915580071627310 -0.1093481802115360 -0.0010601014177568 -0.0000014458228879 -0.0000014938956048  0.0400261494009523  0.0180580974419972  0.0092132504242451 -1.4072088973593200 -1.5212012494801500 0.4079055422317920 0.1599483130475640 -0.0046735359569929 -0.0044253262161005 -1.8571475913759100 -0.4031497826702400 0.0849015681692710 -0.2257128580612920 -0.3307477951183650 -0.2557559184395190 -0.4531985082804610 -0.5341761350472270 0.3646238141279680 0.3603139641158800 0.2932224947572630 0.6001445469340250 0.5039997875438060 0.4668928640936500 0.4088583646551290 0.5248133353055360 0.4440557923094290
    0.1   -0.2464419641482460 -0.2774153233972800 -0.2419849681859750 -0.2159572988522690  0.8837635057027910 -0.1221833768730910  0.2890209915658740 0.3609773912176570 0.6796403235589960 -0.1203234194869740 -0.0095781938365105 -0.0091311877263691 -0.0000017618182496  0.0406923890414978  0.0187576968592212  0.0091770608487944 -1.3775350561906300 -1.5588146355752500 0.3826772642202150 0.1180456788835990 -0.0054981782655166 -0.0044752635101850 -1.6933015535378400 -0.4106809740578840 0.0822852228887146 -0.1971657286502670 -0.3034342387568920 -0.2273780092606650 -0.5595380222575010 -0.5995654008335480 0.3773149612260230 0.3622412109534710 0.3058662966967730 0.5804476608541280 0.5174927775766600 0.4518314029734340 0.4208300424568200 0.5207449309209680 0.4560381766578650
    0.15  -0.0771751272296130 -0.1082252757155910 -0.0939554515669245 -0.0188559515947778  1.1045574548438600 -0.1151312333331240  0.3489251001067520 0.4435666368994170 0.8206717947215570 -0.1478533042267330 -0.0797000195466235 -0.1061400711142910 -0.0116149978331732  0.0385365803750634  0.0208403778461626  0.0084255538167330 -1.3047454734934800 -1.5546509544985100 0.3387081858027680 0.0762391834452875 -0.0060699037646678 -0.0043559591434871 -1.4739793205860400 -0.4462238803701860 0.0708425313555023 -0.2504635484625670 -0.3579852182163120 -0.2973613635520170 -0.7066557777245760 -0.6646730464270010 0.4205159985547740 0.3393429192383280 0.3335166881059750 0.5289137551348660 0.5530955106299720 0.4276458197094800 0.4552933469697380 0.5112791219012840 0.4393051343517960
    0.2    0.0405594808831559 -0.0077282823725784 -0.0329357162076816  0.0977204826995843  1.1425790790134700 -0.1057191168540270  0.3722539227241170 0.5259387014440060 0.8944652896530820 -0.1753118327644590 -0.1628405724059960 -0.1905540130924890 -0.0703516281536629  0.0344218267917848  0.0220145357833909  0.0074084568455730 -1.2525154396822100 -1.5299381829848600 0.2988014581902580 0.0598123873775724 -0.0057279870130134 -0.0038467366062087 -1.3537154633193600 -0.4806650787981650 0.0627269858251427 -0.3514329644238130 -0.4494836594136780 -0.4211846625506190 -0.7761270389945640 -0.6765718066660800 0.4710484094826400 0.3078985636442060 0.3678152527072530 0.4963277349205770 0.5816461579655670 0.4175140424711400 0.4781484644913840 0.5035988500569350 0.4117968194252760
    0.25   0.1161360079386870  0.0455512686241350 -0.0218646332100325  0.1828656137015420  1.1166678356454500 -0.0959115648679502  0.3639273275607390 0.5926458211482060 0.9514471984717970 -0.1975481854813300 -0.2376907309394700 -0.2386263420394340 -0.1392336794544470  0.0301984485118963  0.0220498416898711  0.0063660608238311 -1.2210171934017700 -1.5075909330134600 0.2681747226996620 0.0472484189561765 -0.0050865192380324 -0.0032636166820230 -1.3112990269528600 -0.5135409274151990 0.0616544496255378 -0.4563389214185420 -0.5390065111345010 -0.5398009092490380 -0.8288006277909410 -0.6846682992304260 0.5148599316146770 0.2855216261744740 0.3995944962541640 0.4770587925609880 0.5994129051899660 0.4166683191773280 0.4900244567390270 0.4964417374025240 0.3893046381000030
    0.3    0.1659191261450740  0.0725370613365805 -0.0359674153322261  0.2295701498524820  1.0576588366467200 -0.0882656506919790  0.3427750060884890 0.6483788027762600 0.9819984405493800 -0.2161260130183380 -0.2965674398979590 -0.2665884284153660 -0.2169703936280970  0.0263787728828427  0.0216264161548529  0.0053861646702039 -1.2047472906024600 -1.4854043484828200 0.2441324298126210 0.0419492390586564 -0.0043698926044844 -0.0027135380939124 -1.3252507728285300 -0.5429162086543740 0.0645387790445636 -0.5550263121051320 -0.6210404997811030 -0.6445535318562390 -0.8538221721074140 -0.6735161372595090 0.5463002600989580 0.2736557189233880 0.4272231091987260 0.4656311763164020 0.6091651025639550 0.4221564137529650 0.4957367311495720 0.4906316632512320 0.3720915588780540
    0.4    0.2142056666127370  0.0871536549688902 -0.0785690467168578  0.2764151479005750  0.9207449431454760 -0.0817387187650157  0.2621885450896460 0.7417540614842620 1.0112737345534200 -0.2472511509254110 -0.3436334917221890 -0.2565078736132940 -0.3586252797911450  0.0205765954005230  0.0202875364431140  0.0038382219060837 -1.1921038099281000 -1.4558697162866900 0.2098186797110940 0.0408684583105697 -0.0031642937062858 -0.0017940043857435 -1.4077075423307700 -0.5972162270181300 0.0741639723226930 -0.7281908574894840 -0.7628684799249960 -0.8199077697170760 -0.8746936616440970 -0.6381631348609450 0.5808849727025450 0.2713662162845130 0.4653458134731120 0.4672831153779370 0.6113503193815050 0.4361192706099510 0.4955634501806600 0.4867080815561310 0.3527750902276900
    0.5    0.2236254270212470  0.0737703256835049 -0.1248626176144320  0.2932144086137190  0.8027962857692040 -0.0840244330603874  0.1721136232246120 0.8151053466925040 1.0356710065186700 -0.2717014152455810 -0.3293921568751970 -0.1956967186201360 -0.4758435322483390  0.0165224891710283  0.0187963908607794  0.0026597132484042 -1.1860778618169400 -1.4381584618490300 0.1912179053378480 0.0410520296595116 -0.0023448358088493 -0.0011582034067666 -1.5070859378876100 -0.6493752154999540 0.0836822599658712 -0.8748820619897430 -0.8876408712201270 -0.9615402715827100 -0.8939061858589470 -0.6160880182479380 0.5949464334180670 0.2871764340948960 0.4832505926756100 0.4803914686955640 0.6007190809790290 0.4486042327739210 0.4926763166550150 0.4858212403211350 0.3446261711175850
    0.75   0.1528039303532890 -0.0248167903571809 -0.2511392119124840  0.1388909993170780  0.4519964034477110 -0.1046230174209790  0.0270194376114289 0.9406307668392510 1.0243375273572300 -0.3135419875863270 -0.2250006281710770 -0.0911523105914097 -0.6780831702704660  0.0110013901513618  0.0160522319622777  0.0012402638358105 -1.1698623108011400 -1.3625787842858000 0.1791792655901220 0.0659622332730993 -0.0013043059118461 -0.0005882173264089 -1.5844202517297500 -0.7429284095282450 0.1035767308819100 -1.1534790724423800 -1.1395651591115200 -1.2323996821315000 -0.8389026019711570 -0.5147492098368240 0.5850050231740750 0.3462884754383560 0.4785627709562630 0.5185233324163180 0.5620391824549910 0.4718500465503010 0.4894503194326150 0.4871171137374260 0.3419011444574020
    1.0    0.0183554539383078 -0.1591378376284470 -0.3854397008591480 -0.0815004332093187  0.1288852589717840 -0.1246837038142780 -0.0535877846749373 1.0248278846159400 0.9984729722811390 -0.3393133894939400 -0.1276588419069730 -0.0409136585181734 -0.7992367966752370  0.0086318100105947  0.0146222483242542  0.0009003395366128 -1.1508125147275900 -1.3000691876438900 0.1832396128840250 0.0943261823256111 -0.0008735093977044 -0.0003997330115688 -1.4244083078078700 -0.7989976385952170 0.1185000096002400 -1.3487217771603600 -1.3270174440744400 -1.4337289163009600 -0.7382346855789400 -0.4287560627663270 0.5652851427812200 0.3922029871907690 0.4481274157753080 0.5644306606646860 0.5259679896173710 0.4845488048918390 0.4855760478703810 0.4913162411271670 0.3475742684982780
    1.5   -0.2926406493971360 -0.4394400484356270 -0.6634745672889770 -0.5698164868777540 -0.4777414376471740 -0.1367512471546550 -0.1185422683336340 1.1535846852560400 0.9228592531769220 -0.3551593410006160 -0.0316373719436222 -0.0058305420526171 -0.9286080973093520  0.0062127909966995  0.0114205875168941  0.0006726268670384 -1.1172685240682800 -1.1760450613418900 0.1958900128843000 0.1499938137415910 -0.0005279011472397 -0.0005031399510306 -0.8544827391292060 -0.8438703395779730 0.1413533804677000 -1.5948082564095300 -1.5616885373157400 -1.6940289391677400 -0.5338216528196720 -0.2734691164270120 0.5400623156625950 0.4389989898505710 0.3998380606154830 0.6147869472762440 0.4771405443244140 0.4911661512017220 0.4858319625974600 0.4862020347407820 0.3584781550167080
    2.0   -0.6164896637512180 -0.7252715132235520 -0.9386642110776790 -1.0016397597173700 -0.9827809560644520 -0.1204851699381740 -0.1574596881853990 1.2561590239982100 0.9157149198331690 -0.3487315863272320 -0.0067392342056503 -0.0008274455605290 -0.8998831651883260  0.0045185743588915  0.0076239354167913  0.0004849758370595 -1.0938451612547300 -1.0683876519211600 0.2093417950110930 0.1991110124549130 -0.0003935827881709 -0.0008887392881376 -0.4424325390151640 -0.8536333300862120 0.1558153259573340 -1.7120254817165000 -1.6704563706071200 -1.8185653745450900 -0.4237829724483130 -0.2166062958480880 0.5306044642337280 0.4525458066815850 0.3651681953582200 0.6249992145898750 0.4491015982391830 0.4851846396569770 0.4819819680840680 0.4774435589161110 0.3657798632961100
    3.0   -1.2120217913721900 -1.2593110926431200 -1.4636739356095600 -1.6980520879594500 -1.7669432223057700 -0.0595654650319802 -0.2204723665783100 1.3973296744797800 0.9588403924773120 -0.3233624830738870 -0.0000028831797237 -0.0000043740923315 -0.7774992929692280  0.0001846487026116  0.0015942173971129 -0.0000443776256955 -1.0585068691241300 -0.9286291899300890 0.2337544609389410 0.2596941009305470 -0.0003265684501350 -0.0016673660346856 -0.0238666422441761 -0.8486298188632920 0.1646442443399270 -1.7746560709922100 -1.7136221908604800 -1.8823684494043700 -0.3206735394784300 -0.2094181559654280 0.5341895930662030 0.4630363429223910 0.3632239046532420 0.5759362561116940 0.4215979819838170 0.4631745228225680 0.4732577539251810 0.4497578024830470 0.3748448621655020
    4.0   -1.7187620785302500 -1.7255326287093000 -1.9157987949568300 -2.2378527680411400 -2.3717405638272600  0.0060780094038531 -0.2907358910284120 1.4863934712127500 1.0614239334825600 -0.3008016678137440 -0.0000002303764802 -0.0000003167873542 -0.5992793127354700 -0.0045086409598014 -0.0033339971710007 -0.0004426514054550 -1.0347965137315500 -0.8267625726198150 0.2561912331555940 0.2946206159118700 -0.0002970204994493 -0.0024918478847597  0.0000000000000000 -0.8369401809898650 0.1609560550301920 -1.7432239926968500 -1.6657097551617700 -1.8532526872794200 -0.3155245227823960 -0.2880704899694910 0.5512683175278550 0.4723731595661930 0.3842160013347000 0.5005221059354860 0.4088763842852300 0.4389155701811710 0.4595536649184570 0.4197110255834490 0.3802459556632600
    5.0   -2.2524124481564500 -2.2233337887420500 -2.3988731729506100 -2.7681880158076700 -2.9912308138027000  0.1087794828940540 -0.2475264997327470 1.5711476167331400 1.0248966641608600 -0.2757023074987770 -0.0000002893187016 -0.0000007071111743 -0.6712278770777070 -0.0080289129978441 -0.0055089260712685  0.0002598589919845 -0.9844367319831440 -0.7634431186144020 0.2732908377032170 0.3203152022108220 -0.0006897102389096 -0.0030925027294924  0.0000000000000000 -0.8223177494406110 0.1455355246584370 -1.6392650516693500 -1.5448698990426400 -1.7280816734851900 -0.1970906573510090 -0.2362019597302050 0.5684528701196870 0.4816961813462040 0.4683567199764780 0.4119013474002300 0.4034142608449920 0.4200274542874700 0.4420885624015020 0.3737143966344340 0.3884066340183610
    pgv    2.9029349822540100  2.7442184267612700  2.5956072627404700  2.7208097262709800  3.2025577336977900 -0.1446177480065630 -0.0413092466691142 0.8212932944431650 0.8048031763759270 -0.2099764391081720 -0.0000106980728248 -0.0000492798570503 -0.2820776116949390  0.0155391426948740  0.0171590486230531  0.0030037011458330 -1.2265529440479100 -1.3749132391246600 0.3076583015302820 0.2104730674561660 -0.0009692157684588 -0.0006985849374855 -6.1179459855387300 -0.6707577779339960 0.0957650492780946  0.3935242034563910  0.3928190325309850  0.3150238242701770 -0.3632617170998910 -0.2432876895838630 0.4386543757769160 0.3740824694470210 0.3305136472559800 0.5673397303206320 0.5590865385354610 0.4351807257924570 0.4801642015831750 0.4853170221825470 0.2740663767048480
    pgd    2.4541041890538500  2.3782401415145500  2.2914153189502800  2.0838396593163400  1.9313699400126300 -0.2352916881091410  0.0713994939700537 1.5616444489691000 1.4936921369303000 -0.1676096441841540 -0.0000019923442846 -0.0000232740338163 -0.2069439338171460 -0.0032395363349413  0.0109930765184774  0.0052177204872172 -1.0191698911307200 -1.1559670502824900 0.2068132897445940 0.1789279177790470 -0.0018437138641425 -0.0013634189684089  0.0000000000000000 -0.7422544318623790 0.1490020084340320 -0.4228777481185350 -0.3833592619351370 -0.4612451842659720 -0.3050704862339770 -0.2043152093014790 0.6449844035380140 0.4977962177812710 0.5366022406101780 0.7130676587043830 0.7016130925807040 0.4750313723101500 0.5971604738380890 0.5707298418086840 0.3229783037503560
    """)

    CONST_FAULT = {'C4': 0.3, 'href': 0}

    # subduction or crustal
    SBCR = "_sb"
    SUFFIX = "_if"
    MC = 7.1


class ChaoEtAl2020SSlab(ChaoEtAl2020SInter):
    """
    Chao et al. (2020) for Subduction Slab.
    """
    DEFINED_FOR_TECTONIC_REGION_TYPE = const.TRT.SUBDUCTION_INTRASLAB
    CONST_FAULT = {'C4': 0.2, 'href': 35}
    SUFFIX = "_is"


class ChaoEtAl2020Asc(ChaoEtAl2020SInter):
    """
    Chao et al. (2020) for Crustal.
    """
    DEFINED_FOR_TECTONIC_REGION_TYPE = const.TRT.ACTIVE_SHALLOW_CRUST

    # add rake to determine fault style in _ftype()
    REQUIRES_RUPTURE_PARAMETERS = {'mag', 'rake', 'ztor'}

    CONST_FAULT = {'C4': 0, 'href': 0}

    # subduction or crustal
    SBCR = "_cr"
    SUFFIX = "_cr"
    MC = 7.6
