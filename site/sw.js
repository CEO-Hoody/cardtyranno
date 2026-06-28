// 카드티라노 관심카드 푸시 SW — 백엔드 없이 platform_events.json 로컬 체크
var DB='ctpush',STORE='kv';
function idb(){return new Promise(function(res,rej){var q=indexedDB.open(DB,1);q.onupgradeneeded=function(){q.result.createObjectStore(STORE);};q.onsuccess=function(){res(q.result);};q.onerror=function(){rej(q.error);};});}
function kvGet(k){return idb().then(function(db){return new Promise(function(res){var t=db.transaction(STORE,'readonly').objectStore(STORE).get(k);t.onsuccess=function(){res(t.result);};t.onerror=function(){res(undefined);};});});}
function kvSet(k,v){return idb().then(function(db){return new Promise(function(res){var t=db.transaction(STORE,'readwrite').objectStore(STORE).put(v,k);t.onsuccess=function(){res();};t.onerror=function(){res();};});});}
function _nk2(s){return (s||'').toLowerCase().replace(/[^0-9a-z가-힣]/g,'');}
function won(n){if(!n)return '';if(n>=10000)return (Math.round(n/1000)/10).toString().replace(/\.0$/,'')+'만원';return n.toLocaleString()+'원';}
function curMonthLabel(){return (new Date().getMonth()+1)+'월';}
function fetchEvents(){return fetch('/platform_events.json?t='+Date.now(),{cache:'no-store'}).then(function(r){return r.json();}).catch(function(){return {products:[]};});}
function sigOf(events){var a=(events||[]).filter(function(e){return e.reward_won;}).map(function(e){return (e.platform||'')+':'+e.reward_won;});a.sort();return a.join('|');}
function maxOf(events){var m=0;(events||[]).forEach(function(e){if((e.reward_won||0)>m)m=e.reward_won;});return m;}
function runCheck(mode){ // 'all'(기준선 전체) | 'new'(신규 찜만 기준선) | 'check'(변경 시 알림)
 return Promise.all([kvGet('enabled'),kvGet('favList'),kvGet('seen')]).then(function(v){
  var enabled=v[0],favList=v[1]||[],seen=v[2]||{};
  if(!enabled)return;
  return fetchEvents().then(function(d){
   var byNk={};(d.products||[]).forEach(function(p){byNk[_nk2(p.name)]={sig:sigOf(p.events),max:maxOf(p.events),name:p.name};});
   var notifs=[];
   favList.forEach(function(f){
    var info=byNk[f.nk];if(!info||!info.sig)return;          // 아직 이벤트 없는 카드는 skip
    var prev=seen[f.nk];
    if(mode==='all'){seen[f.nk]=info.sig;return;}            // 알림 켤 때: 현 상태를 조용히 기준선으로
    if(prev===undefined){seen[f.nk]=info.sig;return;}        // 새로 찜한 카드: 조용히 기준선만
    if(mode==='check'&&prev!==info.sig){notifs.push({name:f.name,max:info.max});seen[f.nk]=info.sig;}
   });
   var keep={};favList.forEach(function(f){if(seen[f.nk]!==undefined)keep[f.nk]=seen[f.nk];});  // 찜 해제 카드 정리
   return kvSet('seen',keep).then(function(){
    notifs.forEach(function(n){
     var body=n.name+'에 '+curMonthLabel()+' 캐시백 이벤트가 등록됐어요!'+(n.max?(' 최대 '+won(n.max)):'');
     self.registration.showNotification('관심카드 새 이벤트 🦖',{body:body,tag:'ct-'+_nk2(n.name),renotify:true,data:{url:'/favorites.html'}});
    });
   });
  });
 });
}
self.addEventListener('install',function(e){self.skipWaiting();});
self.addEventListener('activate',function(e){e.waitUntil(self.clients.claim());});
self.addEventListener('message',function(e){var m=e.data||{};
 if(m.type==='enable'){e.waitUntil(Promise.all([kvSet('enabled',1),kvSet('favList',m.favList||[])]).then(function(){return runCheck('all');}));}
 else if(m.type==='test'){e.waitUntil(self.registration.showNotification('🦖 카드티라노 알림 테스트',{body:'관심카드 알림이 정상 동작합니다! 새 이벤트가 등록되면 이렇게 알려드릴게요.',icon:'/og-image.png',badge:'/og-image.png',tag:'ct-test',renotify:true,data:{url:'/favorites.html'}}));}
 else if(m.type==='disable'){e.waitUntil(kvSet('enabled',0));}
 else if(m.type==='sync'){e.waitUntil(kvSet('favList',m.favList||[]).then(function(){return runCheck('new');}));}
 else if(m.type==='check'){e.waitUntil(runCheck('check'));}
});
self.addEventListener('periodicsync',function(e){if(e.tag==='ct-events')e.waitUntil(runCheck('check'));});
self.addEventListener('notificationclick',function(e){e.notification.close();var url=(e.notification.data&&e.notification.data.url)||'/favorites.html';
 e.waitUntil(self.clients.matchAll({type:'window',includeUncontrolled:true}).then(function(cl){for(var i=0;i<cl.length;i++){if(cl[i].url.indexOf('favorites')>=0&&'focus' in cl[i])return cl[i].focus();}if(self.clients.openWindow)return self.clients.openWindow(url);}));
});
