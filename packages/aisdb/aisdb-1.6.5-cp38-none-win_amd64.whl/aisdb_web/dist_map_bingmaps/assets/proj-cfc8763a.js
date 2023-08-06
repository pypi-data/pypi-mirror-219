const w={radians:6370997/(2*Math.PI),degrees:2*Math.PI*6370997/360,ft:.3048,m:1,"us-ft":.3048006096012192};class ln{constructor(r){this.code_=r.code,this.units_=r.units,this.extent_=r.extent!==void 0?r.extent:null,this.worldExtent_=r.worldExtent!==void 0?r.worldExtent:null,this.axisOrientation_=r.axisOrientation!==void 0?r.axisOrientation:"enu",this.global_=r.global!==void 0?r.global:!1,this.canWrapX_=!!(this.global_&&this.extent_),this.getPointResolutionFunc_=r.getPointResolution,this.defaultTileGrid_=null,this.metersPerUnit_=r.metersPerUnit}canWrapX(){return this.canWrapX_}getCode(){return this.code_}getExtent(){return this.extent_}getUnits(){return this.units_}getMetersPerUnit(){return this.metersPerUnit_||w[this.units_]}getWorldExtent(){return this.worldExtent_}getAxisOrientation(){return this.axisOrientation_}isGlobal(){return this.global_}setGlobal(r){this.global_=r,this.canWrapX_=!!(r&&this.extent_)}getDefaultTileGrid(){return this.defaultTileGrid_}setDefaultTileGrid(r){this.defaultTileGrid_=r}setExtent(r){this.extent_=r,this.canWrapX_=!!(this.global_&&r)}setWorldExtent(r){this.worldExtent_=r}setGetPointResolution(r){this.getPointResolutionFunc_=r}getPointResolutionFunc(){return this.getPointResolutionFunc_}}const L=ln,_=6378137,U=Math.PI*_,hn=[-U,-U,U,U],dn=[-180,-85,180,85],G=_*Math.log(Math.tan(Math.PI/2));class b extends L{constructor(r){super({code:r,units:"m",extent:hn,global:!0,worldExtent:dn,getPointResolution:function(t,e){return t/Math.cosh(e[1]/_)}})}}const D=[new b("EPSG:3857"),new b("EPSG:102100"),new b("EPSG:102113"),new b("EPSG:900913"),new b("http://www.opengis.net/def/crs/EPSG/0/3857"),new b("http://www.opengis.net/gml/srs/epsg.xml#3857")];function gn(n,r,t){const e=n.length;t=t>1?t:2,r===void 0&&(t>2?r=n.slice():r=new Array(e));for(let s=0;s<e;s+=t){r[s]=U*n[s]/180;let i=_*Math.log(Math.tan(Math.PI*(+n[s+1]+90)/360));i>G?i=G:i<-G&&(i=-G),r[s+1]=i}return r}function En(n,r,t){const e=n.length;t=t>1?t:2,r===void 0&&(t>2?r=n.slice():r=new Array(e));for(let s=0;s<e;s+=t)r[s]=180*n[s]/U,r[s+1]=360*Math.atan(Math.exp(n[s+1]/_))/Math.PI-90;return r}const mn=6378137,V=[-180,-90,180,90],wn=Math.PI*mn/180;class P extends L{constructor(r,t){super({code:r,units:"degrees",extent:V,axisOrientation:t,global:!0,metersPerUnit:wn,worldExtent:V})}}const k=[new P("CRS:84"),new P("EPSG:4326","neu"),new P("urn:ogc:def:crs:OGC:1.3:CRS84"),new P("urn:ogc:def:crs:OGC:2:84"),new P("http://www.opengis.net/def/crs/OGC/1.3/CRS84"),new P("http://www.opengis.net/gml/srs/epsg.xml#4326","neu"),new P("http://www.opengis.net/def/crs/EPSG/0/4326","neu")];let F={};function yn(){F={}}function Pn(n){return F[n]||F[n.replace(/urn:(x-)?ogc:def:crs:EPSG:(.*:)?(\w+)$/,"EPSG:$3")]||null}function Tn(n,r){F[n]=r}let T={};function Mn(){T={}}function R(n,r,t){const e=n.getCode(),s=r.getCode();e in T||(T[e]={}),T[e][s]=t}function Sn(n,r){let t;return n in T&&r in T[n]&&(t=T[n][r]),t}const u={UNKNOWN:0,INTERSECTING:1,ABOVE:2,RIGHT:4,BELOW:8,LEFT:16},bn={1:"The view center is not defined",2:"The view resolution is not defined",3:"The view rotation is not defined",4:"`image` and `src` cannot be provided at the same time",5:"`imgSize` must be set when `image` is provided",7:"`format` must be set when `url` is set",8:"Unknown `serverType` configured",9:"`url` must be configured or set using `#setUrl()`",10:"The default `geometryFunction` can only handle `Point` geometries",11:"`options.featureTypes` must be an Array",12:"`options.geometryName` must also be provided when `options.bbox` is set",13:"Invalid corner",14:"Invalid color",15:"Tried to get a value for a key that does not exist in the cache",16:"Tried to set a value for a key that is used already",17:"`resolutions` must be sorted in descending order",18:"Either `origin` or `origins` must be configured, never both",19:"Number of `tileSizes` and `resolutions` must be equal",20:"Number of `origins` and `resolutions` must be equal",22:"Either `tileSize` or `tileSizes` must be configured, never both",24:"Invalid extent or geometry provided as `geometry`",25:"Cannot fit empty extent provided as `geometry`",26:"Features must have an id set",27:"Features must have an id set",28:'`renderMode` must be `"hybrid"` or `"vector"`',30:"The passed `feature` was already added to the source",31:"Tried to enqueue an `element` that was already added to the queue",32:"Transformation matrix cannot be inverted",33:"Invalid units",34:"Invalid geometry layout",36:"Unknown SRS type",37:"Unknown geometry type found",38:"`styleMapValue` has an unknown type",39:"Unknown geometry type",40:"Expected `feature` to have a geometry",41:"Expected an `ol/style/Style` or an array of `ol/style/Style.js`",42:"Question unknown, the answer is 42",43:"Expected `layers` to be an array or a `Collection`",47:"Expected `controls` to be an array or an `ol/Collection`",48:"Expected `interactions` to be an array or an `ol/Collection`",49:"Expected `overlays` to be an array or an `ol/Collection`",50:"`options.featureTypes` should be an Array",51:"Either `url` or `tileJSON` options must be provided",52:"Unknown `serverType` configured",53:"Unknown `tierSizeCalculation` configured",55:"The {-y} placeholder requires a tile grid with extent",56:"mapBrowserEvent must originate from a pointer event",57:"At least 2 conditions are required",59:"Invalid command found in the PBF",60:"Missing or invalid `size`",61:"Cannot determine IIIF Image API version from provided image information JSON",62:"A `WebGLArrayBuffer` must either be of type `ELEMENT_ARRAY_BUFFER` or `ARRAY_BUFFER`",64:"Layer opacity must be a number",66:"`forEachFeatureAtCoordinate` cannot be used on a WebGL layer if the hit detection logic has not been enabled. This is done by providing adequate shaders using the `hitVertexShader` and `hitFragmentShader` properties of `WebGLPointsLayerRenderer`",67:"A layer can only be added to the map once. Use either `layer.setMap()` or `map.addLayer()`, not both",68:"A VectorTile source can only be rendered if it has a projection compatible with the view projection",69:"`width` or `height` cannot be provided together with `scale`"};class Un extends Error{constructor(r){const t=bn[r];super(t),this.code=r,this.name="AssertionError",this.message=t}}const Rn=Un;function _n(n,r){if(!n)throw new Rn(r)}function cr(n){const r=K();for(let t=0,e=n.length;t<e;++t)An(r,n[t]);return r}function In(n,r,t){const e=Math.min.apply(null,n),s=Math.min.apply(null,r),i=Math.max.apply(null,n),f=Math.max.apply(null,r);return v(e,s,i,f,t)}function ur(n,r,t){return t?(t[0]=n[0]-r,t[1]=n[1]-r,t[2]=n[2]+r,t[3]=n[3]+r,t):[n[0]-r,n[1]-r,n[2]+r,n[3]+r]}function lr(n,r){return r?(r[0]=n[0],r[1]=n[1],r[2]=n[2],r[3]=n[3],r):n.slice()}function hr(n,r,t){let e,s;return r<n[0]?e=n[0]-r:n[2]<r?e=r-n[2]:e=0,t<n[1]?s=n[1]-t:n[3]<t?s=t-n[3]:s=0,e*e+s*s}function dr(n,r){return Cn(n,r[0],r[1])}function gr(n,r){return n[0]<=r[0]&&r[2]<=n[2]&&n[1]<=r[1]&&r[3]<=n[3]}function Cn(n,r,t){return n[0]<=r&&r<=n[2]&&n[1]<=t&&t<=n[3]}function z(n,r){const t=n[0],e=n[1],s=n[2],i=n[3],f=r[0],a=r[1];let o=u.UNKNOWN;return f<t?o=o|u.LEFT:f>s&&(o=o|u.RIGHT),a<e?o=o|u.BELOW:a>i&&(o=o|u.ABOVE),o===u.UNKNOWN&&(o=u.INTERSECTING),o}function K(){return[1/0,1/0,-1/0,-1/0]}function v(n,r,t,e,s){return s?(s[0]=n,s[1]=r,s[2]=t,s[3]=e,s):[n,r,t,e]}function q(n){return v(1/0,1/0,-1/0,-1/0,n)}function Er(n,r){const t=n[0],e=n[1];return v(t,e,t,e,r)}function mr(n,r,t,e,s){const i=q(s);return Gn(i,n,r,t,e)}function wr(n,r){return n[0]==r[0]&&n[2]==r[2]&&n[1]==r[1]&&n[3]==r[3]}function yr(n,r){return r[0]<n[0]&&(n[0]=r[0]),r[2]>n[2]&&(n[2]=r[2]),r[1]<n[1]&&(n[1]=r[1]),r[3]>n[3]&&(n[3]=r[3]),n}function An(n,r){r[0]<n[0]&&(n[0]=r[0]),r[0]>n[2]&&(n[2]=r[0]),r[1]<n[1]&&(n[1]=r[1]),r[1]>n[3]&&(n[3]=r[1])}function Gn(n,r,t,e,s){for(;t<e;t+=s)Fn(n,r[t],r[t+1]);return n}function Fn(n,r,t){n[0]=Math.min(n[0],r),n[1]=Math.min(n[1],t),n[2]=Math.max(n[2],r),n[3]=Math.max(n[3],t)}function Pr(n,r){let t;return t=r(Q(n)),t||(t=r(Z(n)),t)||(t=r(x(n)),t)||(t=r(j(n)),t)?t:!1}function Tr(n){let r=0;return nn(n)||(r=y(n)*pn(n)),r}function Q(n){return[n[0],n[1]]}function Z(n){return[n[2],n[1]]}function vn(n){return[(n[0]+n[2])/2,(n[1]+n[3])/2]}function Mr(n,r){let t;return r==="bottom-left"?t=Q(n):r==="bottom-right"?t=Z(n):r==="top-left"?t=j(n):r==="top-right"?t=x(n):_n(!1,13),t}function Sr(n,r,t,e,s){const[i,f,a,o,c,d,g,h]=On(n,r,t,e);return v(Math.min(i,a,c,g),Math.min(f,o,d,h),Math.max(i,a,c,g),Math.max(f,o,d,h),s)}function On(n,r,t,e){const s=r*e[0]/2,i=r*e[1]/2,f=Math.cos(t),a=Math.sin(t),o=s*f,c=s*a,d=i*f,g=i*a,h=n[0],m=n[1];return[h-o+g,m-c-d,h-o-g,m-c+d,h+o-g,m+c+d,h+o+g,m+c-d,h-o+g,m-c-d]}function pn(n){return n[3]-n[1]}function br(n,r,t){const e=t||K();return Nn(n,r)?(n[0]>r[0]?e[0]=n[0]:e[0]=r[0],n[1]>r[1]?e[1]=n[1]:e[1]=r[1],n[2]<r[2]?e[2]=n[2]:e[2]=r[2],n[3]<r[3]?e[3]=n[3]:e[3]=r[3]):q(e),e}function j(n){return[n[0],n[3]]}function x(n){return[n[2],n[3]]}function y(n){return n[2]-n[0]}function Nn(n,r){return n[0]<=r[2]&&n[2]>=r[0]&&n[1]<=r[3]&&n[3]>=r[1]}function nn(n){return n[2]<n[0]||n[3]<n[1]}function Ur(n,r){return r?(r[0]=n[0],r[1]=n[1],r[2]=n[2],r[3]=n[3],r):n}function Rr(n,r,t){let e=!1;const s=z(n,r),i=z(n,t);if(s===u.INTERSECTING||i===u.INTERSECTING)e=!0;else{const f=n[0],a=n[1],o=n[2],c=n[3],d=r[0],g=r[1],h=t[0],m=t[1],A=(m-g)/(h-d);let M,S;i&u.ABOVE&&!(s&u.ABOVE)&&(M=h-(m-c)/A,e=M>=f&&M<=o),!e&&i&u.RIGHT&&!(s&u.RIGHT)&&(S=m-(h-o)*A,e=S>=a&&S<=c),!e&&i&u.BELOW&&!(s&u.BELOW)&&(M=h-(m-a)/A,e=M>=f&&M<=o),!e&&i&u.LEFT&&!(s&u.LEFT)&&(S=m-(h-f)*A,e=S>=a&&S<=c)}return e}function Wn(n,r,t,e){if(nn(n))return q(t);let s=[];if(e>1){const a=n[2]-n[0],o=n[3]-n[1];for(let c=0;c<e;++c)s.push(n[0]+a*c/e,n[1],n[2],n[1]+o*c/e,n[2]-a*c/e,n[3],n[0],n[3]-o*c/e)}else s=[n[0],n[1],n[2],n[1],n[2],n[3],n[0],n[3]];r(s,s,2);const i=[],f=[];for(let a=0,o=s.length;a<o;a+=2)i.push(s[a]),f.push(s[a+1]);return In(i,f,t)}function Xn(n,r){const t=r.getExtent(),e=vn(n);if(r.canWrapX()&&(e[0]<t[0]||e[0]>=t[2])){const s=y(t),f=Math.floor((e[0]-t[0])/s)*s;n[0]-=f,n[2]-=f}return n}function _r(n,r){if(r.canWrapX()){const t=r.getExtent();if(!isFinite(n[0])||!isFinite(n[2]))return[[t[0],n[1],t[2],n[3]]];Xn(n,r);const e=y(t);if(y(n)>e)return[[t[0],n[1],t[2],n[3]]];if(n[0]<t[0])return[[n[0]+e,n[1],t[2],n[3]],[t[0],n[1],n[2],n[3]]];if(n[2]>t[2])return[[n[0],n[1],t[2],n[3]],[t[0],n[1],n[2]-e,n[3]]]}return[n]}function H(n,r,t){return Math.min(Math.max(n,r),t)}function Ir(n,r,t,e,s,i){const f=s-t,a=i-e;if(f!==0||a!==0){const o=((n-t)*f+(r-e)*a)/(f*f+a*a);o>1?(t=s,e=i):o>0&&(t+=f*o,e+=a*o)}return Ln(n,r,t,e)}function Ln(n,r,t,e){const s=t-n,i=e-r;return s*s+i*i}function Cr(n){const r=n.length;for(let e=0;e<r;e++){let s=e,i=Math.abs(n[e][e]);for(let a=e+1;a<r;a++){const o=Math.abs(n[a][e]);o>i&&(i=o,s=a)}if(i===0)return null;const f=n[s];n[s]=n[e],n[e]=f;for(let a=e+1;a<r;a++){const o=-n[a][e]/n[e][e];for(let c=e;c<r+1;c++)e==c?n[a][c]=0:n[a][c]+=o*n[e][c]}}const t=new Array(r);for(let e=r-1;e>=0;e--){t[e]=n[e][r]/n[e][e];for(let s=e-1;s>=0;s--)n[s][r]-=n[s][e]*t[e]}return t}function p(n){return n*Math.PI/180}function qn(n,r){const t=n%r;return t*r<0?t+r:t}function Ar(n,r,t){return n+t*(r-n)}function rn(n,r){const t=Math.pow(10,r);return Math.round(n*t)/t}function Gr(n,r){return Math.floor(rn(n,r))}function Fr(n,r){return Math.ceil(rn(n,r))}function vr(n,r){return n[0]+=+r[0],n[1]+=+r[1],n}function Bn(n,r){let t=!0;for(let e=n.length-1;e>=0;--e)if(n[e]!=r[e]){t=!1;break}return t}function Or(n,r){const t=Math.cos(r),e=Math.sin(r),s=n[0]*t-n[1]*e,i=n[1]*t+n[0]*e;return n[0]=s,n[1]=i,n}function pr(n,r){return n[0]*=r,n[1]*=r,n}function $n(n,r){const t=n[0]-r[0],e=n[1]-r[1];return t*t+e*e}function Nr(n,r){return Math.sqrt($n(n,r))}function Wr(n,r){if(r.canWrapX()){const t=y(r.getExtent()),e=tn(n,r,t);e&&(n[0]-=e*t)}return n}function tn(n,r,t){const e=r.getExtent();let s=0;return r.canWrapX()&&(n[0]<e[0]||n[0]>e[2])&&(t=t||y(e),s=Math.floor((n[0]-e[0])/t)),s}const Yn=63710088e-1;function J(n,r,t){t=t||Yn;const e=p(n[1]),s=p(r[1]),i=(s-e)/2,f=p(r[0]-n[0])/2,a=Math.sin(i)*Math.sin(i)+Math.sin(f)*Math.sin(f)*Math.cos(e)*Math.cos(s);return 2*t*Math.atan2(Math.sqrt(a),Math.sqrt(1-a))}const en={info:1,warn:2,error:3,none:4};let Dn=en.info;function Vn(...n){Dn>en.warn||console.warn(...n)}let N=!0;function sn(n){N=!(n===void 0?!0:n)}function O(n,r){if(r!==void 0){for(let t=0,e=n.length;t<e;++t)r[t]=n[t];r=r}else r=n.slice();return r}function B(n,r){if(r!==void 0&&n!==r){for(let t=0,e=n.length;t<e;++t)r[t]=n[t];n=r}return n}function on(n){Tn(n.getCode(),n),R(n,n,O)}function an(n){n.forEach(on)}function E(n){return typeof n=="string"?Pn(n):n||null}function kn(n,r,t,e){n=E(n);let s;const i=n.getPointResolutionFunc();if(i){if(s=i(r,t),e&&e!==n.getUnits()){const f=n.getMetersPerUnit();f&&(s=s*f/w[e])}}else{const f=n.getUnits();if(f=="degrees"&&!e||e=="degrees")s=r;else{const a=I(n,E("EPSG:4326"));if(a===B&&f!=="degrees")s=r*n.getMetersPerUnit();else{let c=[t[0]-r/2,t[1],t[0]+r/2,t[1],t[0],t[1]-r/2,t[0],t[1]+r/2];c=a(c,c,2);const d=J(c.slice(0,2),c.slice(2,4)),g=J(c.slice(4,6),c.slice(6,8));s=(d+g)/2}const o=e?w[e]:n.getMetersPerUnit();o!==void 0&&(s/=o)}}return s}function W(n){an(n),n.forEach(function(r){n.forEach(function(t){r!==t&&R(r,t,O)})})}function fn(n,r,t,e){n.forEach(function(s){r.forEach(function(i){R(s,i,t),R(i,s,e)})})}function zn(){yn(),Mn()}function Hn(n,r){return n?typeof n=="string"?E(n):n:E(r)}function X(n){return function(r,t,e){const s=r.length;e=e!==void 0?e:2,t=t!==void 0?t:new Array(s);for(let i=0;i<s;i+=e){const f=n(r.slice(i,i+e)),a=f.length;for(let o=0,c=e;o<c;++o)t[i+o]=o>=a?r[i+o]:f[o]}return t}}function Jn(n,r,t,e){const s=E(n),i=E(r);R(s,i,X(t)),R(i,s,X(e))}function Kn(n,r){return sn(),C(n,"EPSG:4326",r!==void 0?r:"EPSG:3857")}function Qn(n,r){const t=C(n,r!==void 0?r:"EPSG:3857","EPSG:4326"),e=t[0];return(e<-180||e>180)&&(t[0]=qn(e+180,360)-180),t}function Zn(n,r){if(n===r)return!0;const t=n.getUnits()===r.getUnits();return(n.getCode()===r.getCode()||I(n,r)===O)&&t}function I(n,r){const t=n.getCode(),e=r.getCode();let s=Sn(t,e);return s||(s=B),s}function $(n,r){const t=E(n),e=E(r);return I(t,e)}function C(n,r,t){return $(r,t)(n,void 0,n.length)}function Y(n,r,t,e){const s=$(r,t);return Wn(n,s,void 0,e)}function jn(n,r,t){return I(r,t)(n)}let l=null;function cn(n){l=E(n)}function xn(){l=null}function nr(){return l}function rr(){cn("EPSG:4326")}function tr(n,r){return l?C(n,r,l):n}function er(n,r){return l?C(n,l,r):(N&&!Bn(n,[0,0])&&n[0]>=-180&&n[0]<=180&&n[1]>=-90&&n[1]<=90&&(N=!1,Vn("Call useGeographic() from ol/proj once to work with [longitude, latitude] coordinates.")),n)}function sr(n,r){return l?Y(n,r,l):n}function ir(n,r){return l?Y(n,l,r):n}function or(n,r){if(!l)return n;const t=E(r).getUnits(),e=l.getUnits();return t&&e?n*w[t]/w[e]:n}function ar(n,r){if(!l)return n;const t=E(r).getUnits(),e=l.getUnits();return t&&e?n*w[e]/w[t]:n}function fr(n,r,t){return function(e){let s,i;if(n.canWrapX()){const f=n.getExtent(),a=y(f);e=e.slice(0),i=tn(e,n,a),i&&(e[0]=e[0]-i*a),e[0]=H(e[0],f[0],f[2]),e[1]=H(e[1],f[1],f[3]),s=t(e)}else s=t(e);return i&&r.canWrapX()&&(s[0]+=i*y(r.getExtent())),s}}function un(){W(D),W(k),fn(k,D,gn,En)}un();const Xr=Object.freeze(Object.defineProperty({__proto__:null,METERS_PER_UNIT:w,Projection:L,addCommon:un,addCoordinateTransforms:Jn,addEquivalentProjections:W,addEquivalentTransforms:fn,addProjection:on,addProjections:an,clearAllProjections:zn,clearUserProjection:xn,cloneTransform:O,createProjection:Hn,createSafeCoordinateTransform:fr,createTransformFromCoordinateTransform:X,disableCoordinateWarning:sn,equivalent:Zn,fromLonLat:Kn,fromUserCoordinate:er,fromUserExtent:ir,fromUserResolution:ar,get:E,getPointResolution:kn,getTransform:$,getTransformFromProjections:I,getUserProjection:nr,identityTransform:B,setUserProjection:cn,toLonLat:Qn,toUserCoordinate:tr,toUserExtent:sr,toUserResolution:or,transform:C,transformExtent:Y,transformWithProjections:jn,useGeographic:rr},Symbol.toStringTag,{value:"Module"}));export{lr as $,vn as A,Ln as B,Ar as C,Ir as D,hr as E,Er as F,Cn as G,Pr as H,Gn as I,gr as J,Rr as K,Hn as L,w as M,sn as N,er as O,ir as P,Or as Q,vr as R,tr as S,sr as T,Sr as U,nn as V,Bn as W,Rn as X,br as Y,pr as Z,wr as _,_n as a,Vn as a0,kn as a1,yr as a2,z as a3,u as a4,ur as a5,x as a6,Z as a7,Q as a8,An as a9,rn as aa,Xn as ab,or as ac,_r as ad,$n as ae,cr as af,Nr as ag,Tr as ah,Cr as ai,C as aj,On as ak,Xr as al,H as b,v as c,Fr as d,Gr as e,Kn as f,j as g,E as h,pn as i,y as j,Mr as k,dr as l,Zn as m,qn as n,I as o,Wn as p,Nn as q,B as r,nr as s,p as t,K as u,q as v,Wr as w,Ur as x,$ as y,mr as z};
