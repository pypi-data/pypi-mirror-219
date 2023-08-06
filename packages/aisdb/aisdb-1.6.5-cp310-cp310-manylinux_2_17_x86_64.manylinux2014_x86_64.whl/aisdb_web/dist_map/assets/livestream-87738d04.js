import{f as i}from"./proj-20c50701.js";import{disable_ssl_stream as m,database_hostname as l}from"./constants-36dce06f.js";import{F as u,L as c,b as d,v as n,l as g,a as f}from"./map-0f7724e3.js";import"./main-4e7182f2.js";async function S(){let s=null;m!==null&&m!==void 0?(s=new WebSocket(`ws://${l}:9922`),console.log("Caution: connecting to stream socket without TLS")):s=new WebSocket(`wss://${l}/stream`);const r={};return s.onerror=function(a){s.close(),s.onerror=null,s=null},s.onmessage=function(a){const e=JSON.parse(a.data);let t=r[e.mmsi];if(t===void 0)t=new u({geometry:new c(i([e.lon,e.lat]))}),t.setId(e.mmsi),t.setStyle(d),r[e.mmsi]=t;else{const o=t.getGeometry().getCoordinates();if(o[0]===e.lon&&o[1]===e.lat)return!0;o.push(i([e.lon,e.lat])),t.getGeometry().setCoordinates(o),t.getGeometry().getCoordinates().length>=100&&t.getGeometry().getCoordinates().length%100===0&&t.setGeometry(t.getGeometry().simplify(100)),e.mmsi in n&&(n[e.mmsi].sog_latest=e.sog,n[e.mmsi].heading=e.heading),t.set("meta",{mmsi:e.mmsi}),g.getFeatureById(e.mmsi)===null&&t.getGeometry().getCoordinates().length===2&&(f(t),g.addFeature(t))}return!0},s}export{S as initialize_stream_socket};
