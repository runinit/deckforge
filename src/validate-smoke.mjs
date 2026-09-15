/** The smoke schema is deliberately NOT the future production DeckSpec schema. */
export function validateSmokeDeck(deck) {
  const errors=[];
  const string=(v,p,max=120)=>{if(typeof v!=='string'||!v.trim()||v.length>max)errors.push(`${p}: expected nonempty string <= ${max} characters`);};
  const strings=(v,p,min,max)=>{
    if(!Array.isArray(v)||v.length<min||v.length>max){errors.push(`${p}: expected ${min}..${max} items`);return;}
    v.forEach((s,i)=>string(s,`${p}[${i}]`,52));
  };
  if(!deck||typeof deck!=='object')return ['deck must be an object'];
  if(deck.schemaVersion!=='0.0.1-smoke')errors.push('schemaVersion must be 0.0.1-smoke');
  string(deck.title,'title');
  if(!Array.isArray(deck.slides)||deck.slides.length<1||deck.slides.length>12)return [...errors,'slides: expected 1..12 slides'];
  const ids=new Set();
  deck.slides.forEach((s,i)=>{
    const p=`slides[${i}]`;
    if(!s||typeof s!=='object'){errors.push(`${p}: expected object`);return;}
    string(s.id,`${p}.id`,64);if(ids.has(s.id))errors.push(`${p}: duplicate id`);ids.add(s.id);
    string(s.title,`${p}.title`,88);string(s.notes,`${p}.notes`,1000);
    switch(s.type){
      case 'cover':string(s.subtitle,`${p}.subtitle`,160);break;
      case 'bridge':strings(s.left,`${p}.left`,1,3);strings(s.right,`${p}.right`,1,3);string(s.transition,`${p}.transition`,35);break;
      case 'hub':string(s.center,`${p}.center`,28);strings(s.nodes,`${p}.nodes`,4,4);break;
      case 'layers':strings(s.layers,`${p}.layers`,3,4);break;
      case 'chart':
        strings(s.labels,`${p}.labels`,2,6);
        if(!Array.isArray(s.values)||s.values.length!==s.labels?.length||!s.values.every(v=>typeof v==='number'&&Number.isFinite(v)&&v>=0&&v<=100))errors.push(`${p}.values: numbers in 0..100 matching labels required`);
        if(s.synthetic!==true)errors.push(`${p}.synthetic: the smoke chart must explicitly use synthetic data`);
        break;
      case 'table':
        strings(s.headers,`${p}.headers`,3,3);
        if(!Array.isArray(s.rows)||s.rows.length<1||s.rows.length>5)errors.push(`${p}.rows: expected 1..5 rows`);
        else s.rows.forEach((r,j)=>{if(!Array.isArray(r)||r.length!==3)errors.push(`${p}.rows[${j}]: expected 3 columns`);else r.forEach((v,k)=>string(v,`${p}.rows[${j}][${k}]`,48));});
        break;
      default:errors.push(`${p}: unsupported slide type ${s.type}`);
    }
  });return errors;
}
