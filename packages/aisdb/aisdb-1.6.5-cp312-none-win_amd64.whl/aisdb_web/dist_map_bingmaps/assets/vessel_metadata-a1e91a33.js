import{s as c,v as o,l,a as r}from"./map-17890f38.js";import"./main-f2134a8e.js";import"./proj-cfc8763a.js";import"./constants-b9e7c6db.js";let m=!1;async function _(){for(;m===!1;)await new Promise(e=>setTimeout(e,50))}const y={mmsi:"MMSI",imo:"IMO",vessel_name:"Name",vessel_name2:"Name",flag:"Flag",ship_type_txt:"Type",vesseltype_generic:"Type",vesseltype_detailed:"Details",length_breadth:"Size",year_built:"Year",summer_dwt:"Summer DWT",gross_tonnage:"Gross Tonnage"};function d(e){for(const t in y){const i=e[t];i===""||t.includes("dim_")||t==="ship_type"||t==="vessel_name"&&"vessel_name2"in e||t==="ship_type_txt"&&"vesseltype_generic"in e&&e.vesseltype_generic}const n=e.mmsi;o[n]=e;const a=l.getFeatureById(e.mmsi);return a!==null&&r(a),e}const s=new WebSocket(c);s.addEventListener("message",async e=>{const n=await e.data.text(),a=JSON.parse(n);switch(a.msgtype){case"vesselinfo":{const t=d(a);o[t.mmsi]=t;break}case"doneMetadata":{m=!0,s.close();break}}});s.onerror=()=>{s.close()};s.onopen=async e=>{await s.send(JSON.stringify({msgtype:"meta"})),await _(),s.close()};
