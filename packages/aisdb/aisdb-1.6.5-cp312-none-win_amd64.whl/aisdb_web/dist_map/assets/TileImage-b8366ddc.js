import{i as v,D as z,T as q,c as m,t as f,d as N,e as W,f as $,S as H,g as _,h as V,j as B,E as J,k as y,I as Q,m as ee,R as te}from"./map-0f7724e3.js";import{c as g,d as ie,e as G,h as ne,j as C,k as E,g as S,l as re,m as L,M as se,n as le,o as oe,p as x,q as he}from"./proj-20c50701.js";class ae{constructor(e){this.highWaterMark=e!==void 0?e:2048,this.count_=0,this.entries_={},this.oldest_=null,this.newest_=null}canExpireCache(){return this.highWaterMark>0&&this.getCount()>this.highWaterMark}expireCache(e){for(;this.canExpireCache();)this.pop()}clear(){this.count_=0,this.entries_={},this.oldest_=null,this.newest_=null}containsKey(e){return this.entries_.hasOwnProperty(e)}forEach(e){let t=this.oldest_;for(;t;)e(t.value_,t.key_,this),t=t.newer}get(e,t){const i=this.entries_[e];return g(i!==void 0,15),i===this.newest_||(i===this.oldest_?(this.oldest_=this.oldest_.newer,this.oldest_.older=null):(i.newer.older=i.older,i.older.newer=i.newer),i.newer=null,i.older=this.newest_,this.newest_.newer=i,this.newest_=i),i.value_}remove(e){const t=this.entries_[e];return g(t!==void 0,15),t===this.newest_?(this.newest_=t.older,this.newest_&&(this.newest_.newer=null)):t===this.oldest_?(this.oldest_=t.newer,this.oldest_&&(this.oldest_.older=null)):(t.newer.older=t.older,t.older.newer=t.newer),delete this.entries_[e],--this.count_,t.value_}getCount(){return this.count_}getKeys(){const e=new Array(this.count_);let t=0,i;for(i=this.newest_;i;i=i.older)e[t++]=i.key_;return e}getValues(){const e=new Array(this.count_);let t=0,i;for(i=this.newest_;i;i=i.older)e[t++]=i.value_;return e}peekLast(){return this.oldest_.value_}peekLastKey(){return this.oldest_.key_}peekFirstKey(){return this.newest_.key_}peek(e){if(this.containsKey(e))return this.entries_[e].value_}pop(){const e=this.oldest_;return delete this.entries_[e.key_],e.newer&&(e.newer.older=null),this.oldest_=e.newer,this.oldest_||(this.newest_=null),--this.count_,e.value_}replace(e,t){this.get(e),this.entries_[e].value_=t}set(e,t){g(!(e in this.entries_),16);const i={key_:e,newer:null,older:this.newest_,value_:t};this.newest_?this.newest_.newer=i:this.oldest_=i,this.newest_=i,this.entries_[e]=i,++this.count_}setSize(e){this.highWaterMark=e}}const ce=ae;function j(l,e,t,i){return i!==void 0?(i[0]=l,i[1]=e,i[2]=t,i):[l,e,t]}function R(l,e,t){return l+"/"+e+"/"+t}function A(l){return R(l[0],l[1],l[2])}function ue(l){return l.split("/").map(Number)}function ge(l){return(l[1]<<l[0])+l[2]}function de(l,e){const t=l[0],i=l[1],n=l[2];if(e.getMinZoom()>t||t>e.getMaxZoom())return!1;const r=e.getFullTileRange(t);return r?r.containsXY(i,n):!0}class fe extends ce{clear(){for(;this.getCount()>0;)this.pop().release();super.clear()}expireCache(e){for(;this.canExpireCache()&&!(this.peekLast().getKey()in e);)this.pop().release()}pruneExceptNewestZ(){if(this.getCount()===0)return;const e=this.peekFirstKey(),i=ue(e)[0];this.forEach(n=>{n.tileCoord[0]!==i&&(this.remove(A(n.tileCoord)),n.release())})}}const Z=fe,P={TILELOADSTART:"tileloadstart",TILELOADEND:"tileloadend",TILELOADERROR:"tileloaderror"},F=[0,0,0],d=5;class _e{constructor(e){this.minZoom=e.minZoom!==void 0?e.minZoom:0,this.resolutions_=e.resolutions,g(v(this.resolutions_,function(n,r){return r-n},!0),17);let t;if(!e.origins){for(let n=0,r=this.resolutions_.length-1;n<r;++n)if(!t)t=this.resolutions_[n]/this.resolutions_[n+1];else if(this.resolutions_[n]/this.resolutions_[n+1]!==t){t=void 0;break}}this.zoomFactor_=t,this.maxZoom=this.resolutions_.length-1,this.origin_=e.origin!==void 0?e.origin:null,this.origins_=null,e.origins!==void 0&&(this.origins_=e.origins,g(this.origins_.length==this.resolutions_.length,20));const i=e.extent;i!==void 0&&!this.origin_&&!this.origins_&&(this.origin_=ie(i)),g(!this.origin_&&this.origins_||this.origin_&&!this.origins_,18),this.tileSizes_=null,e.tileSizes!==void 0&&(this.tileSizes_=e.tileSizes,g(this.tileSizes_.length==this.resolutions_.length,19)),this.tileSize_=e.tileSize!==void 0?e.tileSize:this.tileSizes_?null:z,g(!this.tileSize_&&this.tileSizes_||this.tileSize_&&!this.tileSizes_,22),this.extent_=i!==void 0?i:null,this.fullTileRanges_=null,this.tmpSize_=[0,0],this.tmpExtent_=[0,0,0,0],e.sizes!==void 0?this.fullTileRanges_=e.sizes.map(function(n,r){const s=new q(Math.min(0,n[0]),Math.max(n[0]-1,-1),Math.min(0,n[1]),Math.max(n[1]-1,-1));if(i){const o=this.getTileRangeForExtentAndZ(i,r);s.minX=Math.max(o.minX,s.minX),s.maxX=Math.min(o.maxX,s.maxX),s.minY=Math.max(o.minY,s.minY),s.maxY=Math.min(o.maxY,s.maxY)}return s},this):i&&this.calculateTileRanges_(i)}forEachTileCoord(e,t,i){const n=this.getTileRangeForExtentAndZ(e,t);for(let r=n.minX,s=n.maxX;r<=s;++r)for(let o=n.minY,a=n.maxY;o<=a;++o)i([t,r,o])}forEachTileCoordParentTileRange(e,t,i,n){let r,s,o,a=null,h=e[0]-1;for(this.zoomFactor_===2?(s=e[1],o=e[2]):a=this.getTileCoordExtent(e,n);h>=this.minZoom;){if(this.zoomFactor_===2?(s=Math.floor(s/2),o=Math.floor(o/2),r=m(s,s,o,o,i)):r=this.getTileRangeForExtentAndZ(a,h,i),t(h,r))return!0;--h}return!1}getExtent(){return this.extent_}getMaxZoom(){return this.maxZoom}getMinZoom(){return this.minZoom}getOrigin(e){return this.origin_?this.origin_:this.origins_[e]}getResolution(e){return this.resolutions_[e]}getResolutions(){return this.resolutions_}getTileCoordChildTileRange(e,t,i){if(e[0]<this.maxZoom){if(this.zoomFactor_===2){const r=e[1]*2,s=e[2]*2;return m(r,r+1,s,s+1,t)}const n=this.getTileCoordExtent(e,i||this.tmpExtent_);return this.getTileRangeForExtentAndZ(n,e[0]+1,t)}return null}getTileRangeForTileCoordAndZ(e,t,i){if(t>this.maxZoom||t<this.minZoom)return null;const n=e[0],r=e[1],s=e[2];if(t===n)return m(r,s,r,s,i);if(this.zoomFactor_){const a=Math.pow(this.zoomFactor_,t-n),h=Math.floor(r*a),c=Math.floor(s*a);if(t<n)return m(h,h,c,c,i);const u=Math.floor(a*(r+1))-1,w=Math.floor(a*(s+1))-1;return m(h,u,c,w,i)}const o=this.getTileCoordExtent(e,this.tmpExtent_);return this.getTileRangeForExtentAndZ(o,t,i)}getTileRangeForExtentAndZ(e,t,i){this.getTileCoordForXYAndZ_(e[0],e[3],t,!1,F);const n=F[1],r=F[2];this.getTileCoordForXYAndZ_(e[2],e[1],t,!0,F);const s=F[1],o=F[2];return m(n,s,r,o,i)}getTileCoordCenter(e){const t=this.getOrigin(e[0]),i=this.getResolution(e[0]),n=f(this.getTileSize(e[0]),this.tmpSize_);return[t[0]+(e[1]+.5)*n[0]*i,t[1]-(e[2]+.5)*n[1]*i]}getTileCoordExtent(e,t){const i=this.getOrigin(e[0]),n=this.getResolution(e[0]),r=f(this.getTileSize(e[0]),this.tmpSize_),s=i[0]+e[1]*r[0]*n,o=i[1]-(e[2]+1)*r[1]*n,a=s+r[0]*n,h=o+r[1]*n;return G(s,o,a,h,t)}getTileCoordForCoordAndResolution(e,t,i){return this.getTileCoordForXYAndResolution_(e[0],e[1],t,!1,i)}getTileCoordForXYAndResolution_(e,t,i,n,r){const s=this.getZForResolution(i),o=i/this.getResolution(s),a=this.getOrigin(s),h=f(this.getTileSize(s),this.tmpSize_);let c=o*(e-a[0])/i/h[0],u=o*(a[1]-t)/i/h[1];return n?(c=C(c,d)-1,u=C(u,d)-1):(c=E(c,d),u=E(u,d)),j(s,c,u,r)}getTileCoordForXYAndZ_(e,t,i,n,r){const s=this.getOrigin(i),o=this.getResolution(i),a=f(this.getTileSize(i),this.tmpSize_);let h=(e-s[0])/o/a[0],c=(s[1]-t)/o/a[1];return n?(h=C(h,d)-1,c=C(c,d)-1):(h=E(h,d),c=E(c,d)),j(i,h,c,r)}getTileCoordForCoordAndZ(e,t,i){return this.getTileCoordForXYAndZ_(e[0],e[1],t,!1,i)}getTileCoordResolution(e){return this.resolutions_[e[0]]}getTileSize(e){return this.tileSize_?this.tileSize_:this.tileSizes_[e]}getFullTileRange(e){return this.fullTileRanges_?this.fullTileRanges_[e]:this.extent_?this.getTileRangeForExtentAndZ(this.extent_,e):null}getZForResolution(e,t){const i=N(this.resolutions_,e,t||0);return ne(i,this.minZoom,this.maxZoom)}tileCoordIntersectsViewport(e,t){return W(t,0,t.length,2,this.getTileCoordExtent(e))}calculateTileRanges_(e){const t=this.resolutions_.length,i=new Array(t);for(let n=this.minZoom;n<t;++n)i[n]=this.getTileRangeForExtentAndZ(e,n);this.fullTileRanges_=i}}const U=_e;function X(l){let e=l.getDefaultTileGrid();return e||(e=Fe(l),l.setDefaultTileGrid(e)),e}function Te(l,e,t){const i=e[0],n=l.getTileCoordCenter(e),r=M(t);if(!oe(r,n)){const s=L(r),o=Math.ceil((r[0]-n[0])/s);return n[0]+=s*o,l.getTileCoordForCoordAndZ(n,i)}return e}function me(l,e,t,i){i=i!==void 0?i:"top-left";const n=k(l,e,t);return new U({extent:l,origin:le(l,i),resolutions:n,tileSize:t})}function Le(l){const e=l||{},t=e.extent||S("EPSG:3857").getExtent(),i={extent:t,minZoom:e.minZoom,tileSize:e.tileSize,resolutions:k(t,e.maxZoom,e.tileSize,e.maxResolution)};return new U(i)}function k(l,e,t,i){e=e!==void 0?e:$,t=f(t!==void 0?t:z);const n=re(l),r=L(l);i=i>0?i:Math.max(r/t[0],n/t[1]);const s=e+1,o=new Array(s);for(let a=0;a<s;++a)o[a]=i/Math.pow(2,a);return o}function Fe(l,e,t,i){const n=M(l);return me(n,e,t,i)}function M(l){l=S(l);let e=l.getExtent();if(!e){const t=180*se.degrees/l.getMetersPerUnit();e=G(-t,-t,t,t)}return e}class xe extends H{constructor(e){super({attributions:e.attributions,attributionsCollapsible:e.attributionsCollapsible,projection:e.projection,state:e.state,wrapX:e.wrapX,interpolate:e.interpolate}),this.on,this.once,this.un,this.opaque_=e.opaque!==void 0?e.opaque:!1,this.tilePixelRatio_=e.tilePixelRatio!==void 0?e.tilePixelRatio:1,this.tileGrid=e.tileGrid!==void 0?e.tileGrid:null;const t=[256,256];this.tileGrid&&f(this.tileGrid.getTileSize(this.tileGrid.getMinZoom()),t),this.tileCache=new Z(e.cacheSize||0),this.tmpSize=[0,0],this.key_=e.key||"",this.tileOptions={transition:e.transition,interpolate:e.interpolate},this.zDirection=e.zDirection?e.zDirection:0}canExpireCache(){return this.tileCache.canExpireCache()}expireCache(e,t){const i=this.getTileCacheForProjection(e);i&&i.expireCache(t)}forEachLoadedTile(e,t,i,n){const r=this.getTileCacheForProjection(e);if(!r)return!1;let s=!0,o,a,h;for(let c=i.minX;c<=i.maxX;++c)for(let u=i.minY;u<=i.maxY;++u)a=R(t,c,u),h=!1,r.containsKey(a)&&(o=r.get(a),h=o.getState()===_.LOADED,h&&(h=n(o)!==!1)),h||(s=!1);return s}getGutterForProjection(e){return 0}getKey(){return this.key_}setKey(e){this.key_!==e&&(this.key_=e,this.changed())}getOpaque(e){return this.opaque_}getResolutions(e){const t=e?this.getTileGridForProjection(e):this.tileGrid;return t?t.getResolutions():null}getTile(e,t,i,n,r){return V()}getTileGrid(){return this.tileGrid}getTileGridForProjection(e){return this.tileGrid?this.tileGrid:X(e)}getTileCacheForProjection(e){const t=this.getProjection();return g(t===null||x(t,e),68),this.tileCache}getTilePixelRatio(e){return this.tilePixelRatio_}getTilePixelSize(e,t,i){const n=this.getTileGridForProjection(i),r=this.getTilePixelRatio(t),s=f(n.getTileSize(e),this.tmpSize);return r==1?s:B(s,r,this.tmpSize)}getTileCoordForTileUrlFunction(e,t){t=t!==void 0?t:this.getProjection();const i=this.getTileGridForProjection(t);return this.getWrapX()&&t.isGlobal()&&(e=Te(i,e,t)),de(e,i)?e:null}clear(){this.tileCache.clear()}refresh(){this.clear(),super.refresh()}updateCacheSize(e,t){const i=this.getTileCacheForProjection(t);e>i.highWaterMark&&(i.highWaterMark=e)}useTile(e,t,i,n){}}class Ce extends J{constructor(e,t){super(e),this.tile=t}}const Ee=xe;function ye(l,e){const t=/\{z\}/g,i=/\{x\}/g,n=/\{y\}/g,r=/\{-y\}/g;return function(s,o,a){if(s)return l.replace(t,s[0].toString()).replace(i,s[1].toString()).replace(n,s[2].toString()).replace(r,function(){const h=s[0],c=e.getFullTileRange(h);return g(c,55),(c.getHeight()-s[2]-1).toString()})}}function Re(l,e){const t=l.length,i=new Array(t);for(let n=0;n<t;++n)i[n]=ye(l[n],e);return we(i)}function we(l){return l.length===1?l[0]:function(e,t,i){if(!e)return;const n=ge(e),r=he(n,l.length);return l[r](e,t,i)}}function Pe(l){const e=[];let t=/\{([a-z])-([a-z])\}/.exec(l);if(t){const i=t[1].charCodeAt(0),n=t[2].charCodeAt(0);let r;for(r=i;r<=n;++r)e.push(l.replace(t[0],String.fromCharCode(r)));return e}if(t=/\{(\d+)-(\d+)\}/.exec(l),t){const i=parseInt(t[2],10);for(let n=parseInt(t[1],10);n<=i;n++)e.push(l.replace(t[0],n.toString()));return e}return e.push(l),e}class p extends Ee{constructor(e){super({attributions:e.attributions,cacheSize:e.cacheSize,opaque:e.opaque,projection:e.projection,state:e.state,tileGrid:e.tileGrid,tilePixelRatio:e.tilePixelRatio,wrapX:e.wrapX,transition:e.transition,interpolate:e.interpolate,key:e.key,attributionsCollapsible:e.attributionsCollapsible,zDirection:e.zDirection}),this.generateTileUrlFunction_=this.tileUrlFunction===p.prototype.tileUrlFunction,this.tileLoadFunction=e.tileLoadFunction,e.tileUrlFunction&&(this.tileUrlFunction=e.tileUrlFunction),this.urls=null,e.urls?this.setUrls(e.urls):e.url&&this.setUrl(e.url),this.tileLoadingKeys_={}}getTileLoadFunction(){return this.tileLoadFunction}getTileUrlFunction(){return Object.getPrototypeOf(this).tileUrlFunction===this.tileUrlFunction?this.tileUrlFunction.bind(this):this.tileUrlFunction}getUrls(){return this.urls}handleTileChange(e){const t=e.target,i=y(t),n=t.getState();let r;n==_.LOADING?(this.tileLoadingKeys_[i]=!0,r=P.TILELOADSTART):i in this.tileLoadingKeys_&&(delete this.tileLoadingKeys_[i],r=n==_.ERROR?P.TILELOADERROR:n==_.LOADED?P.TILELOADEND:void 0),r!=null&&this.dispatchEvent(new Ce(r,t))}setTileLoadFunction(e){this.tileCache.clear(),this.tileLoadFunction=e,this.changed()}setTileUrlFunction(e,t){this.tileUrlFunction=e,this.tileCache.pruneExceptNewestZ(),typeof t<"u"?this.setKey(t):this.changed()}setUrl(e){const t=Pe(e);this.urls=t,this.setUrls(t)}setUrls(e){this.urls=e;const t=e.join(`
`);this.generateTileUrlFunction_?this.setTileUrlFunction(Re(e,this.tileGrid),t):this.setKey(t)}tileUrlFunction(e,t,i){}useTile(e,t,i){const n=R(e,t,i);this.tileCache.containsKey(n)&&this.tileCache.get(n)}}const Se=p;class pe extends Se{constructor(e){super({attributions:e.attributions,cacheSize:e.cacheSize,opaque:e.opaque,projection:e.projection,state:e.state,tileGrid:e.tileGrid,tileLoadFunction:e.tileLoadFunction?e.tileLoadFunction:je,tilePixelRatio:e.tilePixelRatio,tileUrlFunction:e.tileUrlFunction,url:e.url,urls:e.urls,wrapX:e.wrapX,transition:e.transition,interpolate:e.interpolate!==void 0?e.interpolate:!0,key:e.key,attributionsCollapsible:e.attributionsCollapsible,zDirection:e.zDirection}),this.crossOrigin=e.crossOrigin!==void 0?e.crossOrigin:null,this.tileClass=e.tileClass!==void 0?e.tileClass:Q,this.tileCacheForProjection={},this.tileGridForProjection={},this.reprojectionErrorThreshold_=e.reprojectionErrorThreshold,this.renderReprojectionEdges_=!1}canExpireCache(){if(this.tileCache.canExpireCache())return!0;for(const e in this.tileCacheForProjection)if(this.tileCacheForProjection[e].canExpireCache())return!0;return!1}expireCache(e,t){const i=this.getTileCacheForProjection(e);this.tileCache.expireCache(this.tileCache==i?t:{});for(const n in this.tileCacheForProjection){const r=this.tileCacheForProjection[n];r.expireCache(r==i?t:{})}}getGutterForProjection(e){return this.getProjection()&&e&&!x(this.getProjection(),e)?0:this.getGutter()}getGutter(){return 0}getKey(){let e=super.getKey();return this.getInterpolate()||(e+=":disable-interpolation"),e}getOpaque(e){return this.getProjection()&&e&&!x(this.getProjection(),e)?!1:super.getOpaque(e)}getTileGridForProjection(e){const t=this.getProjection();if(this.tileGrid&&(!t||x(t,e)))return this.tileGrid;const i=y(e);return i in this.tileGridForProjection||(this.tileGridForProjection[i]=X(e)),this.tileGridForProjection[i]}getTileCacheForProjection(e){const t=this.getProjection();if(!t||x(t,e))return this.tileCache;const i=y(e);return i in this.tileCacheForProjection||(this.tileCacheForProjection[i]=new Z(this.tileCache.highWaterMark)),this.tileCacheForProjection[i]}createTile_(e,t,i,n,r,s){const o=[e,t,i],a=this.getTileCoordForTileUrlFunction(o,r),h=a?this.tileUrlFunction(a,n,r):void 0,c=new this.tileClass(o,h!==void 0?_.IDLE:_.EMPTY,h!==void 0?h:"",this.crossOrigin,this.tileLoadFunction,this.tileOptions);return c.key=s,c.addEventListener(ee.CHANGE,this.handleTileChange.bind(this)),c}getTile(e,t,i,n,r){const s=this.getProjection();if(!s||!r||x(s,r))return this.getTileInternal(e,t,i,n,s||r);const o=this.getTileCacheForProjection(r),a=[e,t,i];let h;const c=A(a);o.containsKey(c)&&(h=o.get(c));const u=this.getKey();if(h&&h.key==u)return h;const w=this.getTileGridForProjection(s),O=this.getTileGridForProjection(r),K=this.getTileCoordForTileUrlFunction(a,r),T=new te(s,w,r,O,a,K,this.getTilePixelRatio(n),this.getGutter(),(Y,b,D,I)=>this.getTileInternal(Y,b,D,I,s),this.reprojectionErrorThreshold_,this.renderReprojectionEdges_,this.getInterpolate());return T.key=u,h?(T.interimTile=h,T.refreshInterimChain(),o.replace(c,T)):o.set(c,T),T}getTileInternal(e,t,i,n,r){let s=null;const o=R(e,t,i),a=this.getKey();if(!this.tileCache.containsKey(o))s=this.createTile_(e,t,i,n,r,a),this.tileCache.set(o,s);else if(s=this.tileCache.get(o),s.key!=a){const h=s;s=this.createTile_(e,t,i,n,r,a),h.getState()==_.IDLE?s.interimTile=h.interimTile:s.interimTile=h,s.refreshInterimChain(),this.tileCache.replace(o,s)}return s}setRenderReprojectionEdges(e){if(this.renderReprojectionEdges_!=e){this.renderReprojectionEdges_=e;for(const t in this.tileCacheForProjection)this.tileCacheForProjection[t].clear();this.changed()}}setTileGridForProjection(e,t){const i=S(e);if(i){const n=y(i);n in this.tileGridForProjection||(this.tileGridForProjection[n]=t)}}clear(){super.clear();for(const e in this.tileCacheForProjection)this.tileCacheForProjection[e].clear()}}function je(l,e){l.getImage().src=e}const Ae=pe;export{Ae as T,we as a,j as b,Le as c,M as e};
