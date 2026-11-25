"""Export the approved business flow as matching SVG and PNG (Pillow required)."""
from pathlib import Path
import math
import html
import sys

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    sys.path.insert(0, "/tmp/elyms_diagram_deps")
    from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parents[1] / "docs"
if not OUT.exists():
    OUT.mkdir()
W, H = 1800, 2670
FONT = "/System/Library/Fonts/STHeiti Medium.ttc"
image = Image.new("RGB", (W, H), "white")
draw = ImageDraw.Draw(image)
svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img"><title>订单—收款—退款对账业务流程</title><rect width="100%" height="100%" fill="white"/>']
BLUE, INK, AMBER, BROWN, LINE = "#E6F1FB", "#0C447C", "#FAEEDA", "#633806", "#607587"

def text(x, y, value, size=25, color=INK):
    lines = value.split("\n")
    font = ImageFont.truetype(FONT, size)
    start = y - (len(lines)-1)*(size+10)/2
    for i, line in enumerate(lines):
        yy = start+i*(size+10)
        draw.text((x, yy), line, font=font, fill=color, anchor="mm")
        svg.append(f'<text x="{x}" y="{yy}" text-anchor="middle" dominant-baseline="central" font-family="Heiti SC, PingFang SC, sans-serif" font-size="{size}" fill="{color}">{html.escape(line)}</text>')

def node(x, y, w, h, label, kind="action"):
    fill, stroke = (AMBER, "#854F0B") if kind == "review" else (BLUE, "#185FA5")
    box = (x-w/2, y-h/2, x+w/2, y+h/2)
    if kind == "decision":
        points = [(x,y-h/2),(x+w/2,y),(x,y+h/2),(x-w/2,y)]
        draw.polygon(points, fill="white", outline=stroke, width=2)
        svg.append(f'<polygon points="{" ".join(f"{a},{b}" for a,b in points)}" fill="white" stroke="{stroke}" stroke-width="2"/>')
    else:
        draw.rounded_rectangle(box, radius=20, fill=fill, outline=stroke, width=2)
        svg.append(f'<rect x="{box[0]}" y="{box[1]}" width="{w}" height="{h}" rx="20" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')
    text(x,y,label,25,BROWN if kind=="review" else INK)

def edge(points, label=None, at=None):
    draw.line(points, fill=LINE, width=3)
    svg.append(f'<polyline points="{" ".join(f"{a},{b}" for a,b in points)}" fill="none" stroke="{LINE}" stroke-width="3"/>')
    (x0,y0),(x1,y1)=points[-2:]
    angle=math.atan2(y1-y0,x1-x0)
    arr=[(x1,y1),(x1-15*math.cos(angle-.5),y1-15*math.sin(angle-.5)),(x1-15*math.cos(angle+.5),y1-15*math.sin(angle+.5))]
    draw.polygon(arr,fill=LINE)
    svg.append(f'<polygon points="{" ".join(f"{a},{b}" for a,b in arr)}" fill="{LINE}"/>')
    if label and at:
        font=ImageFont.truetype(FONT,22)
        bounds=draw.textbbox(at,label,font=font,anchor="mm")
        draw.rectangle((bounds[0]-8,bounds[1]-7,bounds[2]+8,bounds[3]+7),fill="white")
        svg.append(f'<rect x="{bounds[0]-8}" y="{bounds[1]-7}" width="{bounds[2]-bounds[0]+16}" height="{bounds[3]-bounds[1]+14}" fill="white"/>')
        text(*at,label,22,LINE)

text(900,55,"订单—收款—退款对账 Agent：业务分支流程",38)
text(900,105,"已确认设计 · 2026-11-25 · 所有补查均受预算约束，预算耗尽即转待复核",23,LINE)
# Edges are painted before boxes so routes terminate cleanly at their borders.
edges = [
 ([(650,215),(650,265)],None,None),
 ([(900,320),(1190,320)],"否",(1040,298)),
 ([(1400,270),(1400,230),(940,230),(940,320),(900,320)],"补充后重判",(1120,230)),
 ([(650,375),(650,425)],"是",(675,400)),
 ([(650,515),(650,570)],None,None),
 ([(900,625),(1190,625)],"否",(1040,602)),
 ([(650,680),(650,745)],"是",(675,712)),
 ([(650,835),(650,900)],None,None),
 ([(900,960),(1190,960)],"缺引用 / 无结果 / 冲突",(1040,935)),
 ([(650,1020),(650,1130)],"是",(675,1060)),
 ([(1400,1010),(1400,1070)],None,None),
 ([(1190,1135),(1100,1135),(1100,1100),(650,1100),(650,1130)],"能确认",(1020,1100)),
 ([(1610,1135),(1720,1135),(1720,960),(1610,960)],"有证据可查且预算允许",(1610,1045)),
 ([(1400,1200),(1400,1265)],"无法确认 / 预算耗尽",(1490,1230)),
 ([(650,1220),(650,1275)],None,None),
 ([(900,1330),(1135,1330),(1135,1040),(1230,1040),(1230,1010)],"有冲突：补查",(1050,1295)),
 ([(650,1385),(650,1450)],"无冲突",(710,1418)),
 ([(650,1550),(650,1610)],None,None),
 ([(900,1670),(1190,1670)],"关联 / 状态不明",(1040,1645)),
 ([(1400,1620),(1400,1580),(950,1580),(950,1500),(910,1500)],"取得证据，重查",(1120,1580)),
 ([(1400,1720),(1400,1810)],"无法查明 / 预算耗尽",(1490,1765)),
 ([(650,1730),(650,1810)],"明确，或无退款",(765,1770)),
 ([(650,1930),(650,2095)],None,None),
 ([(1400,1930),(1400,2095)],None,None),
 ([(1610,1320),(1750,1320),(1750,2010),(1470,2010),(1470,2095)],None,None),
 ([(1025,2205),(1025,2260)],None,None),
 ([(775,2320),(250,2320),(250,790),(390,790)],"遗漏 / 归属冲突：返回查流水",(250,2025)),
 ([(775,2320),(340,2320),(340,1870),(390,1870)],"金额处理错误：重新核算",(545,2285)),
 ([(1025,2380),(1025,2530)],"通过",(1060,2470)),
 ([(1275,2320),(1400,2320),(1400,2390)],"无法修复 / 预算耗尽",(1460,2355)),
 ([(1400,2490),(1400,2530)],None,None),
]
for pts,label,at in edges: edge(pts,label,at)
node(650,175,520,80,"开始：单订单核查 / 账期对账")
node(650,320,500,110,"范围与截止时点明确？","decision")
node(1400,320,420,100,"澄清订单号、账期、截止时点\n等待用户补充","review")
node(650,470,520,90,"查询订单 query_orders\n取得应收、币种与参考号")
node(650,625,500,110,"查到目标订单？","decision")
node(1400,625,420,100,"说明未查到订单\n结束，或由用户修正范围","review")
node(650,790,520,90,"筛选收款 search_receipts\n优先按参考号检索")
node(650,960,500,120,"参考号归属明确\n且证据一致？","decision")
node(1400,960,420,100,"检索候选关联，补查交易凭证\n核对交易号、商户参考号等","review")
node(1400,1135,420,130,"证据足够唯一确认？","decision")
node(1400,1320,420,110,"保留候选，不分配争议流水\n列出需补查的具体字段","review")
node(650,1175,520,90,"确认关联，检查重复通知\ncheck_duplicate_events")
node(650,1330,500,110,"存在冲突通知？","decision")
node(650,1500,520,100,"汇总独立分笔收款，查询退款\nquery_refunds：按原支付交易关联")
node(650,1670,500,120,"退款关联与状态明确？\n查明无退款也可继续","decision")
node(1400,1670,420,100,"补查原支付及退款凭证\n仅使用可见业务证据","review")
node(650,1870,520,120,"按截止时点有效且已观察的记录核算\n成功退款扣净收；处理中退款单列\n分别判断收款是否齐全与退款后净收")
node(1400,1870,420,120,"该项列为待复核\n保留已确认金额\n说明不确定部分与所缺证据","review")
node(1025,2150,1170,110,"汇集各订单结果，整批复核 validate_reconciliation\n检查遗漏订单 / 流水、重复占用、金额及证据；单项异常不阻塞其他订单")
node(1025,2320,500,120,"整批复核通过？","decision")
node(1400,2440,420,100,"标记未完成项及原因\n不宣称整批已核对通过","review")
node(1025,2580,1170,100,"输出：已匹配清单 · 差异清单 · 待复核清单\n附订单、流水与退款证据，以及需要补查的字段")
svg.append('</svg>')
(OUT/"对账Agent业务流程图.svg").write_text("\n".join(svg),encoding="utf-8")
image.save(OUT/"对账Agent业务流程图.png",dpi=(180,180))
print(f"Exported SVG and PNG: {W}x{H}, {OUT}")
