import fs from 'node:fs/promises';
import path from 'node:path';
import { createHash } from 'node:crypto';
import pptxgen from 'pptxgenjs';
import { validateSmokeDeck } from '../src/validate-smoke.mjs';

// Original acceptance-fixture renderer. NOT Astra code and NOT production DeckSpec.
const input=path.resolve(process.argv[2]??'examples/smoke-deck.json');
const out=path.resolve(process.argv[3]??'out/smoke');
const deck=JSON.parse(await fs.readFile(input,'utf8'));
const errors=validateSmokeDeck(deck);
if(errors.length){console.error(errors.join('\n'));process.exit(1);}
await fs.mkdir(out,{recursive:true});
const pptx=new pptxgen();
pptx.defineLayout({name:'DECKFORGE',width:13.3333333333,height:7.5});
pptx.layout='DECKFORGE';pptx.author='Deckforge prototype';pptx.subject='Synthetic acceptance fixture';pptx.title=deck.title;pptx.lang='en-CA';
pptx.theme={headFontFace:'Liberation Sans',bodyFontFace:'Liberation Sans',lang:'en-CA'};
// Demo-only colors: never infer a company palette from these.
const C={bg:'111B25',fg:'F1F3F4',muted:'CAD3DA',accent:'9EE6CE',panel:'203140',line:'4E6575'};
const scene=[];
function box(x,y,w,h){
  if(![x,y,w,h].every(Number.isFinite)||x<0||y<0||w<0||h<0||x+w>13.334||y+h>7.501)throw Error(`Out of bounds: ${[x,y,w,h]}`);
  return {x,y,w,h};
}
function text(s,id,value,x,y,w,h,size=24,options={}){
  s.addText(value,{...box(x,y,w,h),fontFace:'Liberation Sans',fontSize:size,color:C.fg,margin:0,breakLine:false,objectName:id,...options});
  scene.push({slideId:s._dfid,id,type:'text',text:value,x,y,w,h,fontSize:size});
}
function shape(s,id,type,x,y,w,h,options={}){
  s.addShape(type,{...box(x,y,w,h),fill:{color:C.panel},line:{color:C.line,width:1},objectName:id,...options});
  scene.push({slideId:s._dfid,id,type:'shape',geometry:type,x,y,w,h});
}
function line(s,id,x,y,w,h){shape(s,id,pptx.ShapeType.line,x,y,w,h,{line:{color:C.accent,width:2,beginArrowType:'none',endArrowType:'triangle'}});}
function labelPanel(s,id,label,x,y,w,h,accent=false){
  shape(s,`${id}.background`,pptx.ShapeType.rect,x,y,w,h,{fill:{color:accent?C.accent:C.panel},line:{color:accent?C.accent:C.line,width:1}});
  text(s,`${id}.label`,label,x+0.2,y+0.16,w-0.4,h-0.32,23,{color:accent?C.bg:C.fg,bold:accent,align:'center',valign:'mid'});
}
for(const [index,d]of deck.slides.entries()){
  const s=pptx.addSlide();s._dfid=d.id;s.background={color:C.bg};
  text(s,`${d.id}.eyebrow`,'DECKFORGE / SYNTHETIC FIXTURE',0.55,0.25,10,0.25,11,{color:C.accent,charSpacing:1.5});
  if(d.type!=='cover')text(s,`${d.id}.title`,d.title,0.55,0.8,12.2,1.0,34,{bold:true});
  text(s,`${d.id}.footer`,'DEMO BRAND · No customer data · Office review required',0.55,7.02,11.4,0.25,11,{color:C.muted});
  text(s,`${d.id}.number`,String(index+1).padStart(2,'0'),12.05,6.94,0.7,0.38,18,{color:C.accent,align:'right'});
  s.addNotes(d.notes);
  if(d.type==='cover'){
    shape(s,'cover.rule',pptx.ShapeType.rect,0.55,2.04,1.15,0.07,{fill:{color:C.accent},line:{color:C.accent}});
    text(s,'cover.title',d.title,0.55,2.4,10.9,1.6,52,{bold:true});
    text(s,'cover.subtitle',d.subtitle,0.6,4.5,9.8,1.2,25,{color:C.muted});
  } else if(d.type==='bridge'){
    text(s,'bridge.input-heading','INPUT',0.6,2.0,4.0,0.45,19,{color:C.accent,bold:true});
    text(s,'bridge.output-heading','OUTPUT',8.9,2.0,3.8,0.45,19,{color:C.accent,bold:true});
    d.left.forEach((v,i)=>labelPanel(s,`bridge.left.${i}`,v,0.6,2.7+i*1.03,3.85,0.83));
    d.right.forEach((v,i)=>labelPanel(s,`bridge.right.${i}`,v,8.9,2.7+i*1.03,3.83,0.83));
    line(s,'bridge.direction',4.75,3.9,3.75,0);
    text(s,'bridge.transition',d.transition,4.8,3.15,3.7,0.5,22,{align:'center',color:C.accent,bold:true});
    text(s,'bridge.intent','Re-layout, do not flatten',4.7,4.35,3.85,0.7,18,{align:'center',color:C.muted});
  } else if(d.type==='hub'){
    // Horizontal and vertical line primitives: anchoring after manual edits is NOT guaranteed.
    line(s,'hub.edge.left',3.0,4.07,2.45,0);line(s,'hub.edge.right',7.85,4.07,2.5,0);
    line(s,'hub.edge.top',6.65,2.95,0,0.62);line(s,'hub.edge.bottom',6.65,4.6,0,0.9);
    labelPanel(s,'hub.center',d.center,5.35,3.55,2.6,1.05,true);
    [[0.65,3.55],[9.7,3.55],[5.0,2.0],[5.0,5.5]].forEach(([x,y],i)=>labelPanel(s,`hub.node.${i}`,d.nodes[i],x,y,3.0,1.0));
  } else if(d.type==='layers'){
    d.layers.forEach((v,i)=>{
      const x=0.85+i*0.32,w=11.3-i*0.64,y=2.2+i*1.0;
      labelPanel(s,`layers.${i}`,v,x,y,w,0.78,i===3);
    });
  } else if(d.type==='chart'){
    text(s,'chart.disclaimer','ILLUSTRATIVE VALUES — NOT MEASURED PERFORMANCE',0.6,1.82,12.0,0.45,15,{color:C.accent});
    s.addChart(pptx.ChartType.bar,[{name:'Synthetic value',labels:d.labels,values:d.values}],{
      ...box(0.85,2.55,11.8,3.75),catAxisLabelFontFace:'Liberation Sans',catAxisLabelFontSize:18,catAxisLabelColor:C.fg,
      valAxisLabelFontFace:'Liberation Sans',valAxisLabelFontSize:15,valAxisLabelColor:C.muted,
      chartColors:[C.accent],showLegend:false,showTitle:false,showValue:true,dataLabelColor:C.fg,dataLabelPosition:'outEnd',
      showBorder:false,showShadow:false,
      valAxisMinVal:0,valAxisMaxVal:100,valAxisMajorUnit:20,
      showSerName:false,showPercent:false,
      showLine:false,showMarker:false,
      chartArea:{fill:{color:C.bg}},plotArea:{fill:{color:C.bg}},
      valGridLine:{color:C.line,width:0.6},catAxisLineColor:C.line,valAxisLineColor:C.line,
      barDir:'col'
    });
    scene.push({slideId:d.id,id:'chart.native',type:'chart',x:0.85,y:2.55,w:11.8,h:3.75});
  } else if(d.type==='table'){
    s.addTable([d.headers.map(t=>({text:t,options:{bold:true,fill:C.accent,color:C.bg}})),...d.rows],{
      ...box(0.65,2.45,12.0,3.55),colW:[2.25,4.2,5.55],rowH:0.66,
      fontFace:'Liberation Sans',fontSize:22,color:C.fg,fill:C.panel,
      border:{type:'solid',color:C.line,pt:1},margin:0.12,autoPage:false,
    });
    scene.push({slideId:d.id,id:'table.native',type:'table',x:0.65,y:2.45,w:12.0,h:3.55});
  }
}
const fileName=path.join(out,'deck.pptx');
await pptx.writeFile({fileName});
await fs.writeFile(path.join(out,'geometry.json'),JSON.stringify(scene,null,2));
const data=await fs.readFile(fileName);
await fs.writeFile(path.join(out,'build.json'),JSON.stringify({status:'built-not-approved',input,output:fileName,slides:deck.slides.length,pptxSha256:createHash('sha256').update(data).digest('hex'),limitations:['No full text measurement','No unintended-overlap test','No company brand applied','No PowerPoint application verification','No connector anchoring guarantee']},null,2));
console.log(fileName);
