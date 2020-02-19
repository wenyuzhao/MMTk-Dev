import glob
import numpy as np
import sys
import matplotlib.pyplot as plt

# DATA_DIR = './fisher-2020-01-28-Tue-113156'
# DATA_DIR = './fisher-2020-01-30-Thu-122716'
DATA_DIR = './ferret-2020-02-18-Tue-130124'
# HEAP_SIZE = ['2583']#, '6428', '11178', '16833']
HEAP_SIZE = ['2666', '6714', '11714', '17666']
GC = [
    'FastAdaptiveG1PauseAnalysis_STWMark_NoRemSet_NonGen',
    'FastAdaptiveG1PauseAnalysis_STWMark_RemSet_NonGen',
    'FastAdaptiveG1PauseAnalysis_STWMark_RemSet_Gen',
    'FastAdaptiveG1PauseAnalysis_ConcMark_NoRemSet_NonGen',
    'FastAdaptiveG1PauseAnalysis_ConcMark_RemSet_NonGen_Predictor',
    'FastAdaptiveG1PauseAnalysis_ConcMark_RemSet_Gen_Predictor',
]
ID = {
    
    'FastAdaptiveG1PauseAnalysis_STWMark_NoRemSet_NonGen': 'SIM',
    'FastAdaptiveG1PauseAnalysis_STWMark_RemSet_NonGen': 'REM',
    'FastAdaptiveG1PauseAnalysis_STWMark_RemSet_Gen': 'GEN',
    'FastAdaptiveG1PauseAnalysis_ConcMark_NoRemSet_NonGen': 'CMK',
    'FastAdaptiveG1PauseAnalysis_ConcMark_RemSet_NonGen_Predictor': 'G1N',
    'FastAdaptiveG1PauseAnalysis_ConcMark_RemSet_Gen_Predictor': 'G1G',
}


def parseOneFile(file):
    with open(file, encoding='utf-8', errors="surrogateescape") as f:
        startRecording = False
        result = []
        for line in f:
            line = line.strip()
            if line == '===== LatencyTimer Pause Times =====':
                startRecording = True
            elif line == '===== LatencyTimer Pause Times End =====':
                startRecording = False
            elif startRecording and line.isdigit():
                try:
                    result.append(int(line))
                    if f'{result[-1]/1000000:.0f}' == 115:
                        print(file)
                except:
                    pass
        return result

def processOneGCHeapCombo(gc, heap):
    data = []
    file_map = {}
    for file in glob.glob(f'{DATA_DIR}/*.{heap}.*.{gc}.s.wr.log'):
        # if 'pjbb'  in file: continue
        # if 'xalan'  in file: continue
        # if 'pmd' not in file: continue
        try:
            d = parseOneFile(file)
            data += d
            file_map[file] = set(d)
        except:
            e = sys.exc_info()[0]
            print(file)
            raise e
    data = np.array(data)
    if len(data) == 0:
        return None
    print(heap, len(data), np.max(data))
    # evaluate the histogram
    data_sorted = np.sort(data)
    K = f'{gc}.{heap}'
    if K in [
        'FastAdaptiveG1PauseAnalysis_STWMark_RemSet_NonGen.2583',
        'FastAdaptiveG1PauseAnalysis_ConcMark_RemSet_NonGen_Predictor.2583',

    ]:
        print(f'{gc}.{heap} max 10:')
        for v in data_sorted[-30:][::-1]:
            for k, vs in file_map.items():
                if v in vs:
                    print(f'    {v} {k}')
                    break
    # Generate PDF
    # f = plt.figure()
    # p = 1. * np.arange(len(data)) / (len(data) - 1)
    # plt.plot(data_sorted, p)
    # plt.xlabel('$pause time$')
    # plt.ylabel('$p$')
    # f.savefig(f"pdf/{gc}.{heap}.pdf", bbox_inches='tight')
    return {
        'mean': np.mean(data),
        'median': np.percentile(data, 50),
        '95%': np.percentile(data, 95),
        'max':  np.max(data),
    }

def processOneGC(gc):
    result = {}
    for heap in HEAP_SIZE:
        result[heap] = processOneGCHeapCombo(gc, heap)
    return result

def processAll():
    result = {}
    for gc in GC:
        result[gc] = processOneGC(gc)
    return result

def dumpTable(result):
    for gc in GC:
        print(ID[gc] + ' :')
        seq = []
        for key in ['mean', 'median', '95%', 'max']:
            for heap in HEAP_SIZE:
                if result[gc][heap] is None:
                    seq.append('???')
                else:
                    seq.append(f'{result[gc][heap][key]/1000000:.0f}')
        print(' & '.join(seq))

def dumpAnalysis(results):
    calcReductionPercent = lambda old, new: 100 * (old - new) / old
    printReduction = lambda name, oldGC, newGC: print(name + ': ' + ', '.join(
        f"{calcReductionPercent(results[oldGC][h]['95%'], results[newGC][h]['95%']):.2f}%"
        for h in HEAP_SIZE
    ))
    printReduction('Conc Mark', 'FastAdaptiveG1PauseAnalysis_STWMark_NoRemSet_NonGen', 'FastAdaptiveG1PauseAnalysis_ConcMark_NoRemSet_NonGen')
    printReduction('RemSet', 'FastAdaptiveG1PauseAnalysis_STWMark_NoRemSet_NonGen', 'FastAdaptiveG1PauseAnalysis_STWMark_RemSet_NonGen')
    printReduction('Gen', 'FastAdaptiveG1PauseAnalysis_STWMark_RemSet_NonGen', 'FastAdaptiveG1PauseAnalysis_STWMark_RemSet_Gen')



results = processAll()
dumpTable(results)
dumpAnalysis(results)



# 11178 503 [9809116, 9834547, 10015849, 10021783, 10060980, 10119631, 10290374, 10386811, 10399054, 10399681, 10443371, 10502657, 10624954, 10653340, 10712978, 10717413, 10722198, 10753616, 10767434, 10796334, 10815326, 10822317, 10835991, 10858585, 10892655, 10925744, 10943666, 10993816, 11042574, 11077912, 11136965, 11235899, 11370238, 11395042, 11656715, 11817595, 11976908, 12033558, 12168390, 13566006, 14648021, 14722379, 14731357, 14756583, 14788341, 15002677, 15087342, 15157712, 15163416, 15251214, 15269600, 15368738, 15521200, 15535587, 15594247, 15605104, 15689778, 15696396, 15709130, 15777374, 15795752, 15817634, 15847094, 15848292, 15964508, 16020681, 16032833, 16038798, 16097933, 16130996, 16148894, 16192180, 16228118, 16247494, 16359789, 16362434, 16390054, 16395656, 16399783, 16527179, 16576876, 16578890, 16592456, 16625354, 16724146, 16808424, 17132308, 17763335, 17774983, 17994398, 18127895, 18186446, 18555703, 18559404, 18588345, 18638181, 18765910, 18852127, 18863748, 18934787, 19032583, 19054710, 19162756, 19233059, 19379415, 19578490, 19593685, 19736650, 19786543, 19904290, 20398304, 20502688, 20538913, 20557675, 20861337, 21088294, 21559301, 21562202, 22536291, 26673631, 26674232, 26674333, 26679466, 26680099, 26684941, 26685433, 26686898, 26695092, 27895064, 27897445, 27899164, 27900933, 27903554, 27914596, 27915907, 27918259, 27926371, 27929951, 27943350, 27943516, 28098181, 28099680, 28108245, 28109564, 28115676, 28118971, 28123917, 28126570, 28225823, 28248690, 28249661, 28360294, 28387226, 28511834, 28519623, 28524664, 28536433, 28540701, 28563648, 28576049, 28601226, 28697028, 28782469, 28801690, 28816399, 28818497, 28818626, 28819735, 28830467, 28846412, 28847430, 28854021, 28864959, 28904935, 28933755, 29033211, 29039157, 29041196, 29044227, 29044992, 29052191, 29055905, 29094092, 29094713, 29095136, 29098701, 29099206, 29103851, 29106920, 29111738, 29112590, 29194797, 29224727, 29237752, 29245744, 29248732, 29249534, 29251304, 29255605, 29257151, 29259505, 29263933, 29286608, 29370591, 29374544, 29375294, 29378380, 29379016, 29379752, 29381647, 29382346, 29382511, 29392054, 29394775, 29398213, 29411654, 29412010, 29425463, 29427484, 29429202, 29432094, 29447631, 29453585, 29457715, 29484092, 29484190, 29508940, 29566446, 29581781, 29586374, 29607173, 29619029, 29620134, 29632504, 29649023, 29649886, 29663397, 29697213, 29710460, 29713584, 29729434, 29756278, 29879040, 29894793, 29895926, 29901503, 29901678, 29917299, 29918779, 29926302, 29957203, 29957910, 29967039, 29990586, 29995457, 30077866, 30090809, 30098868, 30279135, 30311855, 30316868, 30320064, 30443319, 30447255, 30469158, 30477107, 30478944, 30522581, 30522632, 30532642, 30554304, 30554503, 30578668, 30591800, 30615552, 30620210, 30624762, 30633478, 30636071, 30639836, 30645692, 30773469, 30774484, 30797318, 30805437, 30820168, 30831084, 30833596, 30834811, 30835026, 30845287, 30854428, 30855261, 30861768, 30872703, 31132400, 31314452, 31326551, 31343621, 31345133, 31597137, 31598923, 31661653, 31681297, 31683325, 31702177, 31707060, 31777650, 31942396, 31956839, 31974224, 31976528, 31997809, 32045187, 32053472, 32057292, 32118767, 32127928, 32147238, 32343446, 32376673, 32388395, 32390138, 32395160, 32396188, 32407263, 32410667, 32428209, 32482625, 32488190, 32489492, 32493592, 32494720, 32501408, 32505564, 32776033, 32837849, 32856089, 32863963, 32879851, 32896123, 32903037, 33084798, 33093060, 33093832, 33099816, 33101526, 33109080, 33131025, 33141675, 33142251, 33143706, 33151291, 33151432, 33155262, 33158221, 33164577, 33303516, 33316988, 33434547, 33454359, 33653294, 33654700, 33695493, 33700357, 33747090, 33747382, 33750844, 33753851, 33756573, 33759542, 33764607, 33767172, 34117371, 34120655, 34122784, 34123016, 34125535, 34126918, 34127529, 34128420, 34135939, 34144436, 34310720, 34314131, 34318072, 34321731, 34331108, 34338709, 34339699, 34598004, 34612143, 34654738, 34661028, 34662930, 34663318, 34664399, 34677018, 34680962, 34682438, 34936373, 34957230, 34960857, 34966544, 34968800, 34970287, 34976100, 35582611, 35583216, 35583570, 35587714, 35588089, 35589392, 35595623, 35601065, 36058105, 36062796, 36066627, 36067113, 36069778, 36072781, 36080887, 36084017, 37640543, 37647366, 40559670, 41265899, 41578035, 41895623, 41907181, 42554467, 46682640, 47421010, 47890003, 48051724, 48190443, 48419296, 49029855, 49762338, 51329730, 51837195, 52534590, 53969201, 54377681, 54536757, 54603337, 54732765, 54846562, 58787063, 60032683, 61071010, 61193926, 61227739, 61233356, 61240398, 61332990, 63032002, 63171701, 64321714, 64517637, 64777159, 64917764, 64919287, 64920727, 64923744, 64925611, 64927077, 64929339, 64935542, 70275141, 70281331, 70286538, 70289121, 70290947, 70294546, 70299564, 70300504, 72518025, 72587816, 72826904, 72829097, 72838862, 72839227, 72841002, 72842468, 72849775, 74605709, 75004383, 81238586, 82765724, 83274222, 83590716, 85084635, 85622049, 85649893, 87133482, 87837492, 88787421, 89017387, 89079240, 90282603, 91713118, 92535061]
# 16833 368 [9777004, 9777315, 9981516,  9982209,  10005762, 10011943, 10014081, 10043540, 10068595, 10095764, 10209086, 10251088, 10251410, 10257510, 10299290, 10384171, 10422199, 10465635, 10469500, 10539445, 10565707, 10639205, 10695055, 10770007, 10772131, 10784176, 10843334, 10847940, 10886112, 10895247, 10974716, 10982371, 11023138, 11119515, 11171924, 11393977, 11435105, 11441428, 11564861, 12284182, 15305643, 15395663, 15473360, 15763969, 15826220, 15827382, 15847471, 15973592, 16077979, 16249848, 16267630, 16278350, 16296005, 16300838, 16333697, 16385045, 16414022, 16462314, 16473357, 16532706, 16578629, 16579814, 16589992, 16624073, 16646817, 16717020, 16814836, 16858104, 16873925, 16882361, 16913465, 16930730, 16943956, 16943989, 16944285, 16958480, 17013160, 17120175, 17124289, 17338584, 17373426, 17572842, 17664325, 17724932, 17849477, 17974019, 17981270, 18019578, 18656645, 18783437, 18885904, 19975500, 20025095, 20085527, 20133871, 20166665, 20240238, 20271748, 20340767, 20370380, 20385767, 20781485, 20912032, 20937450, 20967532, 21056528, 21778890, 22020710, 22268974, 27800508, 27832864, 27855422, 28064661, 28072514, 28077351, 28078276, 28081754, 28081890, 28088540, 28094514, 28122248, 28144491, 28930048, 29003219, 29454147, 29455071, 29459241, 29462453, 29466262, 29469555, 29470882, 29472263, 29505299, 29566201, 29582484, 29597231, 29609865, 29662971, 29678516, 29684480, 29852087, 29868801, 29885052, 29890655, 29894991, 29895484, 29895631, 29904998, 29906440, 29990495, 29994925, 29998467, 30001570, 30007562, 30008951, 30010286, 30015462, 30018424, 30022011, 30022047, 30026657, 30067558, 30082571, 30117058, 30131076, 30153015, 30156304, 30305993, 30318823, 30415471, 30431813, 30433819, 30439449, 30440667, 30482570, 30492986, 30624478, 30630350, 30637283, 30638408, 30643686, 30649373, 30650297, 30651213, 30651336, 30661365, 30665511, 30681473, 30777022, 30783109, 30863821, 30871609, 30940338, 31018491, 31018885, 31020772, 31020985, 31028973, 31030278, 31034917, 31049195, 31051985, 31058932, 31081434, 31081623, 31095268, 31102765, 31114693, 31122623, 31137680, 31200508, 31216065, 31276010, 31295204, 31298368, 31343433, 31346272, 31347654, 31348723, 31348986, 31365192, 31472749, 31530316, 31593101, 31610631, 31615482, 31740267, 31765254, 31813493, 31831077, 31836465, 31842069, 31843761, 31845931, 31852045, 31855389, 31857864, 31859586, 31860662, 31909414, 32059636, 32069309, 32086008, 32252155, 32271760, 32403450, 32418871, 32444276, 32470861, 32476630, 32480892, 32486301, 32488177, 32488246, 32489407, 32490934, 32492827, 32494569, 32649686, 32651238, 32655620, 32658677, 32659405, 32662059, 32666936, 32673743, 32702317, 32792181, 32801695, 32835336, 32872163, 32872211, 32881151, 32924950, 33265308, 33267605, 33497769, 33514636, 33522230, 33532874, 33710180, 33809984, 34499718, 34517160, 34519805, 34543973, 34856871, 34858374, 34892672, 34896300, 35555940, 35559118, 35560988, 35571509, 35572349, 35577656, 35581034, 35584248, 36084453, 36090668, 36090731, 36092202, 36093231, 36102164, 36102878, 36103576, 36451457, 36458089, 36462453, 36462559, 36465218, 36709535, 36714697, 36714909, 36715178, 36717223, 36724894, 36725610, 36727330, 37327429, 37330709, 37331246, 37331256, 37338613, 37341031, 37344544, 37345488, 37347419, 37349099, 37353746, 37354864, 38078003, 38099508, 38102537, 38104752, 38106332, 38106768, 38109210, 38109589, 38115601, 38118565, 38123312, 38124760, 39233667, 39234499, 39236252, 39236674, 39245603, 39246422, 39248683, 49654707, 49745079, 49805966, 50133281, 50422871, 50429362, 51163093, 51217476, 51595907, 53222549, 83982726, 85977694, 86397940, 86579233, 88405893, 89519934, 90123455, 90143190]


# 11178 503 [10927536.2,  15289427.600000001, 16370720.0,  19041433.8, 26686165.5,  28316040.799999997, 29037373.200000003, 29263047.400000002, 29506465.0, 29957910.0, 30625633.6, 31611469.0, 32415929.599999998, 33146740.0, 34124275.5, 34959406.2, 41484394.199999996,  61220976.4,         72296272.89999995]
# 16833 368 [10493980.75, 11439531.1,         16386493.85, 16944107.4, 20012696.25, 27835119.8,         29467743.85,        29903124.6,         30153508.35, 30651274.5, 31057889.950000003, 31386703.4, 31887475.6, 32494394.799999997, 33325146.0, 35572013.0, 36714438.9, 37571805.70000001, 39247891.65]