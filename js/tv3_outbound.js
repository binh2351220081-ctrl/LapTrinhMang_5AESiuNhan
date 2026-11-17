
/** TV3 - Tô Đức Thảo. Warehouse dispatch and exact Serial allocation. */
const _dispatchScanSession={orderCode:null,scannedSerials:[]};
let _outboundDraftLines=[],_outboundQuery='',_outboundStatus='ALL',_outboundUnitQuery='';
const _outboundRoles={ADMIN:'SYSTEM_ADMIN',KHO:'WAREHOUSE_MANAGER',NHANVIEN_KHO:'OPERATIONS_STAFF',KETOAN:'ACCOUNTANT',OWNER:'STORE_OWNER'};
const _outboundStateLabels={DRAFT:'Nháp',RESERVED:'Đã giữ chỗ',PACKING:'Đang soạn',COMPLETED:'Đã xuất',CANCELLED:'Đã hủy',DELIVERED:'Đã nhận'};
function _todayIso(){const d=new Date();return `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')}`;}
function _nowTimestamp(){return new Date().toISOString();}
function _outboundEsc(v){return String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));}
function _outboundClone(v){return JSON.parse(JSON.stringify(v));}
function _outboundAssert(ok,message){if(!ok)throw new Error(message);}
function _outboundActor(){let id=null;if(typeof AppState!=='undefined'&&AppState.currentUser)id=AppState.currentUser.id;if(!id){try{id=JSON.parse(localStorage.getItem(OUTBOUND_SESSION_KEY)||'null')?.accountId;}catch(_){}}const a=ChronoDB.getAccounts().find(a=>a.id===id&&a.status==='ACTIVE');return a?{...a,role:_outboundRoles[a.role]||a.role}:null;}
function _outboundCan(...roles){const a=_outboundActor();return !!a&&roles.includes(a.role);}
function _outboundRequire(...roles){const a=_outboundActor();_outboundAssert(a,'Vui lòng đăng nhập demo để tác nghiệp kho.');_outboundAssert(roles.includes(a.role),'Tài khoản không có quyền thực hiện thao tác này.');return a;}
function _outboundId(prefix,rows){const used=new Set(rows.map(r=>r.id||r.code));let i=1,id;do{id=`${prefix}-${new Date().getFullYear()}-${String(i++).padStart(4,'0')}`;}while(used.has(id));return id;}
function _outboundLog(s,a,action,target){s.logs.unshift({time:_nowTimestamp(),user:a.fullName,actorId:a.id,role:a.role,action,target});}
function _outboundGood(s){return !['DISPLAY','DEFECT','DEFECTIVE'].includes(s.qualityType)&&!['DISPLAY','DEFECT','DEFECTIVE'].includes(s.status);}
function _outboundPhysical(state,sku){return state.serials.filter(s=>s.sku===sku&&['IN_STOCK','RESERVED','ALLOCATED','DISPLAY','DEFECT','DEFECTIVE'].includes(s.status)).length;}
function _outboundCard(state,actor,type,ref,serials,delta,note){const groups=new Map();serials.forEach(s=>{if(!groups.has(s.sku))groups.set(s.sku,[]);groups.get(s.sku).push(s);});groups.forEach((group,sku)=>{const w=ChronoDB.getWatchBySku(sku);state.stockCards.unshift({id:_outboundId('TK',state.stockCards),date:_nowTimestamp(),watchId:w?.id||'',sku,watchName:w?.name||group[0].watchName||sku,refType:type,refCode:ref,changeQty:delta*group.length,balanceAfter:_outboundPhysical(state,sku),serialNumber:group.map(s=>s.serialNumber).join(', '),user:actor.fullName,note});});}
const WarehouseOutbound={
 async transact(roles,work){const run=()=>{const actor=_outboundRequire(...roles);return ChronoDB.outboundTransaction(state=>work(state,actor));};if(typeof navigator!=='undefined'&&navigator.locks?.request)return navigator.locks.request('chronovault-outbound-v3',{mode:'exclusive'},run);return run();},
 signIn(username,password){const a=ChronoDB.getAccounts().find(a=>a.username===username.trim()&&a.status==='ACTIVE');_outboundAssert(a?.demoPassword&&password===a.demoPassword,'Sai tài khoản/mật khẩu demo. Dùng thao_outbound, tam_manager hoặc owner_boss / 123.');localStorage.setItem(OUTBOUND_SESSION_KEY,JSON.stringify({accountId:a.id,signedInAt:_nowTimestamp()}));if(typeof AppState!=='undefined')AppState.currentUser={id:a.id};return _outboundActor();},
 signOut(){localStorage.removeItem(OUTBOUND_SESSION_KEY);if(typeof AppState!=='undefined')AppState.currentUser=null;},
 async saveUnit(input){return this.transact(['OPERATIONS_STAFF','WAREHOUSE_MANAGER','STORE_OWNER'],(s,a)=>{const name=String(input.shopName||'').trim(),address=String(input.address||'').trim(),representative=String(input.representative||'').trim(),phone=String(input.phone||'').trim();_outboundAssert(name&&address&&representative&&phone,'Nhập đủ tên, địa chỉ nhận, người phụ trách và số điện thoại.');const old=s.dealers.find(d=>d.id===input.id),taxCode=String(input.taxCode||'').trim();_outboundAssert(!taxCode||!s.dealers.some(d=>d.id!==old?.id&&d.taxCode===taxCode),'Mã số đơn vị/mã số thuế đã tồn tại.');const status=input.status||old?.status||'ACTIVE';_outboundAssert(['ACTIVE','LOCKED','SUSPENDED'].includes(status),'Trạng thái không hợp lệ.');_outboundAssert((old?.status||'ACTIVE')===status||['WAREHOUSE_MANAGER','STORE_OWNER'].includes(a.role),'Chỉ thủ kho/chủ kho được đổi trạng thái đơn vị.');const unit={...(old||{id:_outboundId('DV',s.dealers),tier:'BRONZE',discountRate:0,creditLimit:0,currentDebt:0,availableCredit:0}),shopName:name,name,address,representative,phone,taxCode,status,updatedBy:a.id,updatedAt:_nowTimestamp()};if(old)s.dealers[s.dealers.indexOf(old)]=unit;else s.dealers.push(unit);_outboundLog(s,a,old?'CẬP_NHẬT_ĐƠN_VỊ_NHẬN':'THÊM_ĐƠN_VỊ_NHẬN',`${unit.id}: ${name}`);return unit.id;});},
 async createDraft(dealerId,inputs,note){return this.transact(['OPERATIONS_STAFF','WAREHOUSE_MANAGER','STORE_OWNER'],(s,a)=>{const d=s.dealers.find(d=>d.id===dealerId);_outboundAssert(d?.status==='ACTIVE','Đơn vị nhận phải đang hoạt động.');_outboundAssert(Array.isArray(inputs)&&inputs.length,'Thêm ít nhất một mặt hàng.');const seen=new Set();const items=inputs.map(input=>{const w=ChronoDB.getWatchById(input.watchId);_outboundAssert(w&&w.status!=='DISCONTINUED','Mặt hàng không còn hoạt động.');_outboundAssert(!seen.has(w.sku),'SKU đã có trong lệnh.');seen.add(w.sku);const qty=Number(input.quantity),rate=Number(w.conversionRate||1);_outboundAssert(Number.isSafeInteger(qty)&&qty>0,'Số lượng phải là số nguyên dương.');_outboundAssert(['BOX','PIECE'].includes(input.unit),'Đơn vị tính không hợp lệ.');_outboundAssert(Number.isSafeInteger(rate)&&rate>0,'Hệ số quy đổi sản phẩm không hợp lệ.');const convertedQty=qty*(input.unit==='BOX'?rate:1);_outboundAssert(Number.isSafeInteger(convertedQty),'Số lượng quy đổi quá lớn.');_outboundAssert(convertedQty>=Number(w.minimumDispatchQuantity||1),'Chưa đạt định mức xuất của sản phẩm.');return{watchId:w.id,sku:w.sku,name:w.name,unit:input.unit,quantity:qty,conversionRate:rate,convertedQty,reservedSerials:[],dispatchedSerials:[]};});const o={code:_outboundId('DS',s.orders),dealerId,dealerName:d.shopName,businessType:'WAREHOUSE',date:_todayIso(),createdAt:_nowTimestamp(),createdBy:a.id,createdByName:a.fullName,status:'DRAFT',items,note:String(note||'').trim(),totalAmount:0,assetValuation:0,depositAmount:0,remainingDebt:0,shippingFee:0,scannedSerials:[]};s.orders.unshift(o);_outboundLog(s,a,'LẬP_LỆNH_XUẤT_NHÁP',o.code);return o.code;});},
 async approve(code){return this.transact(['WAREHOUSE_MANAGER','STORE_OWNER'],(s,a)=>{const o=s.orders.find(o=>o.code===code);_outboundAssert(o,'Không tìm thấy lệnh.');if(['RESERVED','PACKING'].includes(o.status)&&!o.reservationIssue)return code;_outboundAssert(o.status==='DRAFT'||!!o.reservationIssue,'Chỉ duyệt lệnh nháp hoặc lệnh cần phân bổ lại.');_outboundAssert(s.dealers.find(d=>d.id===o.dealerId)?.status==='ACTIVE','Đơn vị nhận đã ngừng tiếp nhận.');const plan=[];o.items.forEach(i=>{const pool=s.serials.filter(x=>x.sku===i.sku&&_outboundGood(x)&&(x.status==='IN_STOCK'||['RESERVED','ALLOCATED'].includes(x.status)&&x.orderCode===code)).sort((a,b)=>(a.receivedDate||'').localeCompare(b.receivedDate||'')||(a.receiptCode||'').localeCompare(b.receiptCode||'')||a.serialNumber.localeCompare(b.serialNumber));const other=s.orders.filter(x=>x.code!==code&&['RESERVED','PACKING'].includes(x.status)&&x.reservationIssue).reduce((n,x)=>n+x.items.filter(y=>y.sku===i.sku).reduce((m,y)=>m+(y.convertedQty||y.quantity),0),0);_outboundAssert(pool.length-other>=i.convertedQty,`Không đủ Serial khả dụng ${i.sku}: còn ${Math.max(0,pool.length-other)}, cần ${i.convertedQty}.`);plan.push({item:i,serials:pool.slice(0,i.convertedQty)});});plan.forEach(({item,serials})=>{item.reservedSerials=serials.map(x=>x.serialNumber);serials.forEach(x=>{x.status='RESERVED';x.orderCode=code;});});Object.assign(o,{status:'RESERVED',approvedBy:a.id,approvedByName:a.fullName,approvedAt:_nowTimestamp(),reservationIssue:null,businessType:'WAREHOUSE'});_outboundLog(s,a,'DUYỆT_GIỮ_CHỖ_XUẤT_KHO',code);return code;});},
 async cancel(code,reason){return this.transact(['OPERATIONS_STAFF','WAREHOUSE_MANAGER','STORE_OWNER'],(s,a)=>{const o=s.orders.find(o=>o.code===code);_outboundAssert(o,'Không tìm thấy lệnh.');if(o.status==='CANCELLED')return code;_outboundAssert(['DRAFT','RESERVED'].includes(o.status),'Chỉ hủy lệnh nháp hoặc chưa đóng kiện.');_outboundAssert(String(reason||'').trim(),'Nhập lý do hủy.');s.serials.filter(x=>x.orderCode===code&&['RESERVED','ALLOCATED'].includes(x.status)).forEach(x=>{x.status='IN_STOCK';x.orderCode=null;});Object.assign(o,{status:'CANCELLED',cancelledBy:a.id,cancelReason:reason.trim(),cancelledAt:_nowTimestamp()});o.items.forEach(i=>i.reservedSerials=[]);_outboundLog(s,a,'HỦY_LỆNH_XUẤT',`${code}: ${reason.trim()}`);return code;});},
 async startPacking(code){return this.transact(['OPERATIONS_STAFF','WAREHOUSE_MANAGER','STORE_OWNER'],(s,a)=>{const o=s.orders.find(o=>o.code===code);_outboundAssert(o&&['RESERVED','PACKING'].includes(o.status),'Lệnh chưa được duyệt.');_outboundAssert(!o.reservationIssue,'Thủ kho cần phân bổ lại Serial.');_outboundAssert(o.items.every(i=>(i.reservedSerials||[]).length===i.convertedQty),'Phân bổ chưa đủ Serial.');if(o.status==='PACKING')return code;Object.assign(o,{status:'PACKING',packingBy:a.id,packingByName:a.fullName,packingAt:_nowTimestamp(),scannedSerials:[]});_outboundLog(s,a,'BẮT_ĐẦU_SOẠN_HÀNG',code);return code;});},
 validateScan(s,code,input,already){const o=s.orders.find(o=>o.code===code);_outboundAssert(o&&o.status==='PACKING','Lệnh không ở trạng thái đang soạn.');const sn=String(input||'').trim().toUpperCase();_outboundAssert(sn,'Nhập hoặc quét Serial.');_outboundAssert(!already.includes(sn),`Serial ${sn} đã được quét.`);const x=s.serials.find(x=>x.serialNumber.toUpperCase()===sn);_outboundAssert(x,'Serial không tồn tại.');const item=o.items.find(i=>i.sku===x.sku);_outboundAssert(item,'Serial không đúng SKU trên lệnh.');_outboundAssert((item.reservedSerials||[]).includes(x.serialNumber),'Serial không thuộc Picking List của lệnh.');_outboundAssert(['RESERVED','ALLOCATED'].includes(x.status)&&x.orderCode===code&&_outboundGood(x),'Serial không còn đủ điều kiện xuất.');_outboundAssert(already.length<o.items.reduce((n,i)=>n+i.convertedQty,0),'Đã quét đủ số lượng.');return x;},
 async scan(code,input){return this.transact(['OPERATIONS_STAFF','WAREHOUSE_MANAGER','STORE_OWNER'],(s,a)=>{const o=s.orders.find(o=>o.code===code),already=o?.scannedSerials||[],x=this.validateScan(s,code,input,already);o.scannedSerials=[...already,x.serialNumber];o.lastScannedBy=a.id;return x.serialNumber;});},
 async complete(code,carrier,trackingNumber,shippingFee){return this.transact(['WAREHOUSE_MANAGER','STORE_OWNER'],(s,a)=>{const o=s.orders.find(o=>o.code===code);_outboundAssert(o,'Không tìm thấy lệnh.');if(o.status==='COMPLETED'){const prior=s.dispatches.find(d=>d.orderCode===code);_outboundAssert(prior,'Lệnh lịch sử đã xuất, không thể xuất lại.');return prior.id;}_outboundAssert(o.status==='PACKING','Lệnh chưa được soạn hàng.');const expected=o.items.flatMap(i=>i.reservedSerials||[]),scanned=o.scannedSerials||[];_outboundAssert(expected.length>0&&new Set(scanned).size===expected.length&&expected.every(sn=>scanned.includes(sn)),'Phải quét đủ 100% Serial được phân bổ.');const serials=expected.map(sn=>{const x=s.serials.find(x=>x.serialNumber===sn);_outboundAssert(x&&['RESERVED','ALLOCATED'].includes(x.status)&&x.orderCode===code&&_outboundGood(x),`Serial ${sn} không còn đủ điều kiện xuất.`);return x;});const fee=Number(shippingFee||0);_outboundAssert(Number.isFinite(fee)&&fee>=0,'Chi phí vận chuyển không hợp lệ.');const timestamp=_nowTimestamp(),id=_outboundId('PX',s.dispatches);const doc={id,orderCode:code,businessType:'WAREHOUSE',dealerId:o.dealerId,dealerName:o.dealerName,date:timestamp,status:'DISPATCHED',createdBy:o.createdByName||'',approvedBy:o.approvedByName||'',dispatchedBy:a.fullName,dispatchedById:a.id,carrier:String(carrier||'').trim(),trackingNumber:String(trackingNumber||'').trim(),shippingFee:fee,items:_outboundClone(o.items),serials:serials.map(x=>({serialNumber:x.serialNumber,sku:x.sku,watchName:x.watchName||ChronoDB.getWatchBySku(x.sku)?.name||x.sku,sourceLocation:x.shelfLocation,unitCost:Number(x.costPrice||0),receivedDate:x.receivedDate})),note:o.note||''};doc.assetValuation=doc.serials.reduce((n,x)=>n+x.unitCost,0);serials.forEach(x=>{Object.assign(x,{status:'DISPATCHED',dealerId:o.dealerId,orderCode:code,dispatchCode:id,dispatchedAt:timestamp,shelfLocation:`Đang bàn giao: ${o.dealerName}`});x.timeline=x.timeline||[];x.timeline.push({date:timestamp,title:'Xuất kho',desc:`${id} → ${o.dealerName}; ${a.fullName}`});});Object.assign(o,{status:'COMPLETED',dispatchCode:id,dispatchedAt:timestamp,dispatchedBy:a.id,assetValuation:doc.assetValuation,shippingFee:fee,carrier:doc.carrier,trackingNumber:doc.trackingNumber,businessType:'WAREHOUSE'});o.items.forEach(i=>i.dispatchedSerials=[...i.reservedSerials]);s.dispatches.unshift(doc);_outboundCard(s,a,'XUẤT_KHO',id,serials,-1,`${code} → ${o.dealerName}`);_outboundLog(s,a,'XÁC_NHẬN_XUẤT_KHO',`${id}: ${expected.join(', ')}`);return id;});},
 async handover(code,receivedBy){return this.transact(['WAREHOUSE_MANAGER','STORE_OWNER'],(s,a)=>{const d=s.dispatches.find(d=>d.orderCode===code);_outboundAssert(d,'Không tìm thấy phiếu xuất.');if(d.status==='DELIVERED')return d.id;_outboundAssert(String(receivedBy||'').trim(),'Nhập người ký nhận.');Object.assign(d,{status:'DELIVERED',receivedBy:receivedBy.trim(),receivedAt:_nowTimestamp(),handoverConfirmedBy:a.fullName});d.serials.forEach(row=>{const x=s.serials.find(x=>x.serialNumber===row.serialNumber);if(x?.dispatchCode===d.id&&x.status==='DISPATCHED'){x.status='DELIVERED';x.shelfLocation=`Đơn vị nhận: ${d.dealerName}`;}});_outboundLog(s,a,'XÁC_NHẬN_BÀN_GIAO',`${d.id}: ${d.receivedBy}`);return d.id;});},
 checkReturnOrigin(s,dealerId,x){_outboundAssert(['DISPATCHED','DELIVERED','SOLD'].includes(x.status),'Serial chưa xuất hoặc đã nhận trả.');_outboundAssert(x.dealerId===dealerId,'Serial không thuộc đơn vị đã nhận.');const history=s.dispatches.find(d=>d.dealerId===dealerId&&d.serials.some(y=>y.serialNumber===x.serialNumber));const legacy=s.orders.find(o=>o.dealerId===dealerId&&o.status==='COMPLETED'&&(o.items||[]).some(i=>(i.dispatchedSerials||[]).includes(x.serialNumber)));_outboundAssert(history||legacy,'Chưa có chứng từ xuất gốc cho đơn vị này.');},
 async requestReturn(dealerId,input,condition,location,reason){return this.transact(['OPERATIONS_STAFF','WAREHOUSE_MANAGER','STORE_OWNER'],(s,a)=>{const sn=String(input||'').trim().toUpperCase(),x=s.serials.find(x=>x.serialNumber.toUpperCase()===sn),d=s.dealers.find(d=>d.id===dealerId);_outboundAssert(d&&x,'Chọn đúng đơn vị và Serial.');this.checkReturnOrigin(s,dealerId,x);_outboundAssert(['NEW','DEFECT'].includes(condition),'Kết quả kiểm định không hợp lệ.');const shelf=ChronoDB.getShelves().find(x=>x.id===location);_outboundAssert(shelf,'Chọn vị trí kho đang quản lý.');_outboundAssert(condition==='DEFECT'?shelf.id==='C-01':shelf.id!=='C-01','Kho đích không phù hợp kiểm định.');_outboundAssert(String(reason||'').trim(),'Nhập lý do/kết quả kiểm định.');_outboundAssert(!s.returns.some(r=>r.serial===x.serialNumber&&r.status==='DRAFT'),'Serial đã có phiếu trả đang chờ.');const r={id:_outboundId('TS',s.returns),dealerId,dealerName:d.shopName,serial:x.serialNumber,sku:x.sku,watchId:ChronoDB.getWatchBySku(x.sku)?.id||'',watchName:x.watchName,originDispatch:x.dispatchCode||x.orderCode,condition,location,reason:reason.trim(),date:_nowTimestamp(),status:'DRAFT',businessType:'WAREHOUSE',createdBy:a.fullName};s.returns.unshift(r);_outboundLog(s,a,'LẬP_PHIẾU_HOÀN_TRẢ',r.id);return r.id;});},
 async approveReturn(id){return this.transact(['WAREHOUSE_MANAGER','STORE_OWNER'],(s,a)=>{const r=s.returns.find(r=>r.id===id);_outboundAssert(r,'Không tìm thấy phiếu trả.');if(r.status==='COMPLETED')return id;_outboundAssert(r.status==='DRAFT','Phiếu không còn chờ xác nhận.');const x=s.serials.find(x=>x.serialNumber===r.serial);_outboundAssert(x,'Serial không tồn tại.');this.checkReturnOrigin(s,r.dealerId,x);Object.assign(x,{status:r.condition==='NEW'?'IN_STOCK':'DEFECT',qualityType:r.condition,shelfLocation:r.location,lastDispatchCode:x.dispatchCode||x.orderCode,dispatchCode:null,dealerId:null,orderCode:null});x.timeline=x.timeline||[];x.timeline.push({date:_nowTimestamp(),title:'Nhận hoàn trả',desc:`${id}: ${r.dealerName} → ${r.location}`});Object.assign(r,{status:'COMPLETED',approvedBy:a.fullName,approvedAt:_nowTimestamp()});_outboundCard(s,a,'HOÀN_TRẢ_KHO',id,[x],1,r.reason);_outboundLog(s,a,'XÁC_NHẬN_HOÀN_TRẢ',id);return id;});},
 async requestOther(serialNumber,purpose,reason){return this.transact(['OPERATIONS_STAFF','WAREHOUSE_MANAGER','STORE_OWNER'],(s,a)=>{const x=s.serials.find(x=>x.serialNumber===serialNumber);_outboundAssert(x,'Serial không tồn tại.');_outboundAssert(['DEFECT','DEFECTIVE','DISPLAY'].includes(x.status)||x.status==='IN_STOCK'&&x.qualityType==='DISPLAY','Chỉ chọn hàng lỗi/trưng bày chưa giữ chỗ.');_outboundAssert(['WARRANTY','DISPOSE','LIQUIDATION'].includes(purpose),'Mục đích không hợp lệ.');_outboundAssert(String(reason||'').trim(),'Nhập lý do/biên bản kỹ thuật.');_outboundAssert(!s.otherDispatches.some(r=>(r.serials||[]).includes(serialNumber)&&r.status==='DRAFT'),'Serial đã có phiếu xuất khác chờ duyệt.');const r={id:_outboundId('XK',s.otherDispatches),type:purpose,serials:[serialNumber],sku:x.sku,watchId:ChronoDB.getWatchBySku(x.sku)?.id||'',watchName:x.watchName,date:_nowTimestamp(),reason:reason.trim(),createdBy:a.fullName,status:'DRAFT',businessType:'WAREHOUSE'};s.otherDispatches.unshift(r);_outboundLog(s,a,'LẬP_PHIẾU_XUẤT_KHÁC',r.id);return r.id;});},
 async approveOther(id){const before=ChronoDB.readOutboundState().otherDispatches.find(r=>r.id===id);_outboundAssert(before,'Không tìm thấy phiếu.');return this.transact(before.type==='DISPOSE'?['STORE_OWNER']:['WAREHOUSE_MANAGER','STORE_OWNER'],(s,a)=>{const r=s.otherDispatches.find(r=>r.id===id);if(r.status==='COMPLETED')return id;_outboundAssert(r.status==='DRAFT','Phiếu không còn chờ duyệt.');const serials=r.serials.map(sn=>{const x=s.serials.find(x=>x.serialNumber===sn);_outboundAssert(x&&(['DEFECT','DEFECTIVE','DISPLAY'].includes(x.status)||x.status==='IN_STOCK'&&x.qualityType==='DISPLAY'),'Serial đã thay đổi trạng thái.');return x;});serials.forEach(x=>{x.status=r.type==='WARRANTY'?'WARRANTY':r.type==='LIQUIDATION'?'LIQUIDATED':'DESTROYED';x.shelfLocation=r.type==='WARRANTY'?'Trung tâm bảo hành hãng':r.type==='LIQUIDATION'?'Đã xuất bán thanh lý (Display)':'Đã tiêu hủy';x.timeline=x.timeline||[];x.timeline.push({date:_nowTimestamp(),title:'Xuất khác',desc:`${id}: ${r.reason}`});});Object.assign(r,{status:'COMPLETED',approvedBy:a.fullName,approvedAt:_nowTimestamp()});_outboundCard(s,a,r.type==='WARRANTY'?'XUẤT_BẢO_HÀNH':r.type==='LIQUIDATION'?'XUẤT_THANH_LÝ':'XUẤT_HỦY',id,serials,-1,r.reason);_outboundLog(s,a,'DUYỆT_XUẤT_KHÁC',id);return id;});}
};
function calcReservedQtyForSku(sku){return ChronoDB.inventoryForSku(sku).reserved;}
function calcPhysicalInStockForSku(sku){return ChronoDB.inventoryForSku(sku).physical;}
function buildSmartPickingList(sku,orderCode){const s=ChronoDB.readOutboundState(),o=s.orders.find(o=>o.code===orderCode),names=o?o.items.flatMap(i=>i.reservedSerials||[]):null;return s.serials.filter(x=>x.sku===sku&&_outboundGood(x)&&(names?names.includes(x.serialNumber):x.status==='IN_STOCK')).sort((a,b)=>(a.receivedDate||'').localeCompare(b.receivedDate||'')||a.serialNumber.localeCompare(b.serialNumber)).map((serial,idx)=>({fifoRank:idx+1,serial}));}
function validateScannedSerialForOrderWeb(input,o,already){try{return{valid:true,serial:WarehouseOutbound.validateScan(ChronoDB.readOutboundState(),o.code,input,already.map(x=>typeof x==='string'?x:x.serialNumber))};}catch(e){return{valid:false,message:e.message};}}
function evaluateOutboundOrderWeb(dealer,watch,unit,qtyInput){const qty=Number(qtyInput),rate=Number(watch?.conversionRate||1),convertedQty=qty*(unit==='BOX'?rate:1),stock=watch?ChronoDB.inventoryForSku(watch.sku):{physical:0,reserved:0,available:0},valid=Number.isSafeInteger(qty)&&qty>0&&Number.isSafeInteger(convertedQty)&&['PIECE','BOX'].includes(unit);const reason=!dealer||dealer.status!=='ACTIVE'?'Đơn vị nhận không hoạt động.':!valid?'Số lượng phải là số nguyên dương.':convertedQty>stock.available?'Không đủ Serial khả dụng.':null;return{qty,convertedQty,physicalStock:stock.physical,reservedQty:stock.reserved,availableStock:stock.available,canSubmit:!reason,rejectionReason:reason};}
function _outboundButton(label,action,id,kind='btn-action-small'){return `<button type="button" class="${kind}" data-id="${_outboundEsc(id)}" onclick="${action}(this.dataset.id)">${label}</button>`;}
function _outboundField(label,id,value='',type='text'){return `<label class="form-group"><span class="form-label">${label}</span><input class="form-input" id="${id}" type="${type}" value="${_outboundEsc(value)}"></label>`;}
function _outboundModal(title,body){const t=document.getElementById('generalModalTitle'),b=document.getElementById('generalModalBody'),m=document.getElementById('generalDetailModal');if(!t||!b||!m)return;t.textContent=title;b.innerHTML=body;m.classList.add('active');}
function _outboundRefresh(){renderOutboundTab();if(typeof renderProductsList==='function')renderProductsList();if(typeof renderWarehouseTab==='function')renderWarehouseTab();if(typeof renderDashboard==='function')renderDashboard();}
async function _outboundAction(work,success,after){if(_outboundAction.busy)return;_outboundAction.busy=true;document.querySelectorAll('[data-outbound-submit]').forEach(b=>b.disabled=true);try{const result=await work();if(success&&typeof showToast==='function')showToast(success,'success');if(after)after(result);else closeModal('generalDetailModal');_outboundRefresh();return result;}catch(e){if(typeof showToast==='function')showToast(e.message,'danger');else console.error(e);}finally{_outboundAction.busy=false;document.querySelectorAll('[data-outbound-submit]').forEach(b=>b.disabled=false);}}
function renderOutboundTab(){
 const list=document.getElementById('outboundOrdersList'),units=document.getElementById('dealersOverviewList');if(!list&&!units)return;
 const state=ChronoDB.readOutboundState(),actor=_outboundActor(),operate=_outboundCan('OPERATIONS_STAFF','WAREHOUSE_MANAGER','STORE_OWNER'),manage=_outboundCan('WAREHOUSE_MANAGER','STORE_OWNER');
 if(list){const filtered=state.orders.filter(o=>(_outboundStatus==='ALL'||o.status===_outboundStatus)&&`${o.code} ${o.dealerName} ${(o.items||[]).map(i=>i.sku+' '+i.name).join(' ')}`.toLowerCase().includes(_outboundQuery.toLowerCase()));
  list.innerHTML=`<div class="outbound-toolbar"><div><b>${actor?_outboundEsc(actor.fullName)+' · '+_outboundEsc(actor.role):'Chưa đăng nhập tác nghiệp'}</b><small>Phiên demo cục bộ · dữ liệu lưu trên trình duyệt</small></div><button class="btn-toggle-view" onclick="${actor?'signOutOutbound()':'openOutboundSessionModal()'}">${actor?'Đăng xuất':'Đăng nhập demo'}</button></div>
  <div class="outbound-toolbar"><input aria-label="Tìm lệnh xuất" class="form-input" placeholder="Tìm mã lệnh, đơn vị, SKU" value="${_outboundEsc(_outboundQuery)}" onchange="_outboundQuery=this.value;renderOutboundTab()"><select aria-label="Lọc trạng thái lệnh" class="form-select" onchange="_outboundStatus=this.value;renderOutboundTab()"><option value="ALL">Tất cả trạng thái</option>${Object.entries(_outboundStateLabels).filter(([k])=>k!=='DELIVERED').map(([k,v])=>`<option value="${k}" ${_outboundStatus===k?'selected':''}>${v}</option>`).join('')}</select>${operate?'<button class="btn-primary-action" onclick="openCreateOrderModal()">+ Lệnh xuất</button>':''}</div>
  <div class="outbound-kpis"><span>${state.orders.length} lệnh</span><span>${state.orders.filter(o=>['RESERVED','PACKING'].includes(o.status)).reduce((n,o)=>n+o.items.reduce((m,i)=>m+(i.convertedQty||i.quantity),0),0)} chiếc giữ chỗ</span><span>${(state.dispatches||[]).length} phiếu xuất</span></div>
  ${filtered.map(o=>`<article class="outbound-document-card"><div class="outbound-toolbar"><b>${_outboundEsc(o.code)}</b><span class="badge-status">${_outboundStateLabels[o.status]||_outboundEsc(o.status)}</span></div><p>${_outboundEsc(o.dealerName)} · ${_outboundEsc(o.createdAt||o.date)}</p><p>${(o.items||[]).map(i=>`${_outboundEsc(i.name||i.sku)}: <b>${i.convertedQty||i.quantity} chiếc</b>`).join('<br>')}</p>${o.reservationIssue?`<p class="outbound-error">${_outboundEsc(o.reservationIssue)}</p>`:''}<div class="outbound-actions">${_outboundButton('Xem','viewOrderDetail',o.code)}${manage&&(o.status==='DRAFT'||o.reservationIssue)?_outboundButton('Duyệt giữ chỗ','approveOutboundOrder',o.code):''}${operate&&['DRAFT','RESERVED'].includes(o.status)?_outboundButton('Hủy lệnh','cancelOutboundOrder',o.code):''}${operate&&['RESERVED','PACKING'].includes(o.status)&&!o.reservationIssue?_outboundButton('Soạn / quét Serial','confirmDispatchOrder',o.code):''}${o.status==='COMPLETED'?_outboundButton('In phiếu A4','printDispatchA4',o.code):''}${manage&&o.status==='COMPLETED'&&state.dispatches.some(d=>d.orderCode===o.code&&d.status!=='DELIVERED')?_outboundButton('Xác nhận đã nhận hàng','confirmOutboundHandover',o.code):''}</div></article>`).join('')||'<p>Không có lệnh phù hợp.</p>'}
  <h3>Phiếu hoàn trả và xuất khác</h3>${[...state.returns.filter(r=>r.businessType==='WAREHOUSE'),...state.otherDispatches.filter(r=>r.businessType==='WAREHOUSE')].sort((a,b)=>b.date.localeCompare(a.date)).map(r=>`<article class="outbound-document-card"><b>${_outboundEsc(r.id)}</b> · ${_outboundStateLabels[r.status]||_outboundEsc(r.status)}<p>${_outboundEsc(r.serial||(r.serials||[]).join(', '))} · ${_outboundEsc(r.reason)}</p>${r.status==='DRAFT'&&(r.id.startsWith('TS')?manage:r.type==='DISPOSE'?_outboundCan('STORE_OWNER'):manage)?_outboundButton('Xác nhận phiếu',r.id.startsWith('TS')?'approveOutboundReturn':'approveOutboundOther',r.id):''}</article>`).join('')||'<p>Chưa có phiếu mới.</p>'}`;
 }
 if(units){const filtered=state.dealers.filter(d=>`${d.shopName} ${d.id} ${d.phone} ${d.address}`.toLowerCase().includes(_outboundUnitQuery.toLowerCase()));units.innerHTML=`<div class="outbound-toolbar"><input aria-label="Tìm đơn vị nhận" class="form-input" value="${_outboundEsc(_outboundUnitQuery)}" placeholder="Tìm đơn vị nhận" onchange="_outboundUnitQuery=this.value;renderOutboundTab()">${operate?'<button class="btn-toggle-view" onclick="openOutboundUnitEditor()">+ Đơn vị nhận</button>':''}</div>${filtered.map(d=>`<article class="outbound-document-card"><b>${_outboundEsc(d.shopName)}</b> · ${_outboundEsc(d.id)} <span class="badge-status">${_outboundEsc(d.status)}</span><p>${_outboundEsc(d.address)}<br>${_outboundEsc(d.representative||'Chưa có người phụ trách')} · ${_outboundEsc(d.phone)}</p><div class="outbound-actions">${operate?_outboundButton('Sửa hồ sơ','openOutboundUnitEditor',d.id)+_outboundButton('Lập phiếu hoàn trả','openCustomerReturnModal',d.id):''}</div></article>`).join('')}`;}
}
function openOutboundSessionModal(){_outboundModal('Đăng nhập demo tác nghiệp kho',`<p>Phiên demo trên máy này. Tài khoản: <b>thao_outbound</b> (nhân viên), <b>tam_manager</b> (thủ kho), <b>owner_boss</b> (chủ kho). Mật khẩu demo: <b>123</b>.</p>${_outboundField('Tên tài khoản','outboundUsername')}${_outboundField('Mật khẩu demo','outboundPassword','','password')}<button class="btn-primary-action" onclick="signInOutbound()">Đăng nhập demo</button>`);}
function signInOutbound(){try{WarehouseOutbound.signIn(document.getElementById('outboundUsername').value,document.getElementById('outboundPassword').value);closeModal('generalDetailModal');_outboundRefresh();}catch(e){showToast(e.message,'danger');}}
function signOutOutbound(){WarehouseOutbound.signOut();_outboundRefresh();}
function openOutboundUnitEditor(id){try{_outboundRequire('OPERATIONS_STAFF','WAREHOUSE_MANAGER','STORE_OWNER');const d=ChronoDB.getDealerById(id)||{};_outboundModal(id?'Sửa đơn vị nhận':'Thêm đơn vị nhận',`${_outboundField('Tên đơn vị','unitName',d.shopName)}${_outboundField('Địa chỉ nhận','unitAddress',d.address)}${_outboundField('Người phụ trách','unitContact',d.representative)}${_outboundField('Số điện thoại','unitPhone',d.phone)}${_outboundField('Mã số đơn vị / MST (nếu có)','unitTaxCode',d.taxCode)}<label class="form-label">Trạng thái<select class="form-select" id="unitStatus" ${!_outboundCan('WAREHOUSE_MANAGER','STORE_OWNER')?'disabled':''}>${['ACTIVE','LOCKED','SUSPENDED'].map(s=>`<option ${s===(d.status||'ACTIVE')?'selected':''}>${s}</option>`).join('')}</select></label><button data-outbound-submit class="btn-primary-action" data-id="${_outboundEsc(id||'')}" onclick="saveOutboundUnit(this.dataset.id)">Lưu hồ sơ</button>`);}catch(e){showToast(e.message,'danger');}}
function saveOutboundUnit(id){return _outboundAction(()=>WarehouseOutbound.saveUnit({id,shopName:document.getElementById('unitName').value,address:document.getElementById('unitAddress').value,representative:document.getElementById('unitContact').value,phone:document.getElementById('unitPhone').value,taxCode:document.getElementById('unitTaxCode').value,status:document.getElementById('unitStatus').value}),'Đã lưu đơn vị nhận.');}
function openCreateOrderModal(){
 try{
  _outboundRequire('OPERATIONS_STAFF','WAREHOUSE_MANAGER','STORE_OWNER');
  const modalEl = document.getElementById('createOrderModal');
  const dSel = document.getElementById('orderDealerSelect');
  const wSel = document.getElementById('orderWatchSelect');
  if (modalEl && dSel && wSel) {
   const dealers = ChronoDB.getDealers().filter(d => d.status === 'ACTIVE');
   const watches = ChronoDB.getWatches().filter(w => w.status !== 'DISCONTINUED');
   dSel.innerHTML = dealers.map(d => `<option value="${_outboundEsc(d.id)}">${_outboundEsc(d.shopName || d.name)} (${d.tier || 'VIP'} - ${(Number(d.discountRate||d.discountPercent||0.25)*100).toFixed(0)}%)</option>`).join('');
   wSel.innerHTML = watches.map(w => `<option value="${_outboundEsc(w.id)}">${_outboundEsc(w.name)} (${_outboundEsc(w.sku)}) - Khả dụng ${ChronoDB.inventoryForSku(w.sku).available} chiếc</option>`).join('');
   updateOrderCalculationPreview();
   modalEl.classList.add('active');
   return;
  }
  _outboundDraftLines=[];
  _renderOutboundDraft();
 }catch(e){
  if (typeof showToast==='function') showToast(e.message,'warning');
  else alert(e.message);
 }
}

function submitCreateOrder(){
 const draftDealer = document.getElementById('draftDealer');
 if (draftDealer) {
  return _outboundAction(()=>WarehouseOutbound.createDraft(draftDealer.value,_outboundDraftLines,document.getElementById('draftNote')?.value),'Đã lưu lệnh nháp.');
 }
 const dealerId = document.getElementById('orderDealerSelect')?.value;
 const watchId = document.getElementById('orderWatchSelect')?.value;
 const unit = document.getElementById('orderUnitSelect')?.value || 'PIECE';
 const qty = Number(document.getElementById('orderQtyInput')?.value || 1);
 const deposit = Number(document.getElementById('orderDepositInput')?.value || 0);

 const dealer = ChronoDB.getDealerById(dealerId);
 const watch = ChronoDB.getWatchById(watchId);
 if (!dealer || !watch) {
  if (typeof showToast==='function') showToast('Chọn đầy đủ đại lý và mẫu đồng hồ.', 'warning');
  return;
 }
 const lines = [{ watchId, unit, quantity: qty }];
 return _outboundAction(async () => {
  const code = await WarehouseOutbound.createDraft(dealerId, lines, 'Lệnh điều phối xuất kho B2B');
  const appCode = await WarehouseOutbound.approve(code);
  if (deposit > 0) {
   ChronoDB.outboundTransaction(s => {
    const o = s.orders.find(o => o.code === appCode);
    if (o) {
     o.depositAmount = deposit;
     o.remainingDebt = Math.max(0, (o.totalAmount || 0) - deposit);
    }
   });
  }
  closeModal('createOrderModal');
  return appCode;
 }, 'Đã duyệt lệnh và khóa giữ chỗ tồn kho (RESERVED)!');
}
function openCreateOrderWithWatch(watchId){openCreateOrderModal();const s=document.getElementById('draftWatch');if(s)s.value=watchId;}
function updateOrderCalculationPreview(){
 const preview = document.getElementById('orderCalculationPreview');
 if (!preview) return;
 const dId = document.getElementById('orderDealerSelect')?.value;
 const wId = document.getElementById('orderWatchSelect')?.value;
 const unit = document.getElementById('orderUnitSelect')?.value || 'PIECE';
 const qty = Number(document.getElementById('orderQtyInput')?.value || 1);
 const deposit = Number(document.getElementById('orderDepositInput')?.value || 0);

 const dealer = ChronoDB.getDealerById(dId);
 const watch = ChronoDB.getWatchById(wId);
 if (!dealer || !watch) return;

 const rate = Number(watch.conversionRate || 10);
 const convertedQty = qty * (unit === 'BOX' ? rate : 1);
 const wholesalePrice = Number(watch.price || watch.wholesalePrice || 350000000);
 const discountRate = Number(dealer.discountRate || dealer.discountPercent || 0.25);
 const effectivePrice = wholesalePrice * (1.0 - discountRate);
 const totalValuation = effectivePrice * convertedQty;
 const newLiability = Math.max(0, totalValuation - deposit);
 const currentDebt = Number(dealer.currentDebt || 0);
 const creditLimit = Number(dealer.creditLimit || 3000000000);
 const projectedDebt = currentDebt + newLiability;
 const isOver = projectedDebt > creditLimit;

 preview.innerHTML = `<div style="background:${isOver ? '#fef2f2' : '#f0fdf4'}; border:1px solid ${isOver ? '#f87171' : '#86efac'}; border-radius:6px; padding:10px; font-size:12px;">
   <div><b>Quy đổi:</b> ${qty} ${unit === 'BOX' ? 'thùng' : 'chiếc'} = <b>${convertedQty} chiếc</b> (Định mức MOQ: ${watch.minimumDispatchQuantity || 2} chiếc)</div>
   <div><b>Chiết khấu đại lý (${dealer.tier || 'VIP'}):</b> ${(discountRate * 100).toFixed(0)}% • Đơn giá sau CK: ${_outboundFormatVND(effectivePrice)}</div>
   <div><b>Tổng giá trị đơn:</b> <b>${_outboundFormatVND(totalValuation)}</b></div>
   <div><b>Dư nợ hiện tại:</b> ${_outboundFormatVND(currentDebt)} • <b>Hạn mức:</b> ${_outboundFormatVND(creditLimit)}</div>
   <div><b>Dư nợ dự kiến sau duyệt:</b> <b style="color:${isOver ? '#dc2626' : '#16a34a'};">${_outboundFormatVND(projectedDebt)}</b></div>
   ${isOver ? `<div style="color:#b91c1c; font-weight:bold; margin-top:4px;">⚠️ CẢNH BÁO: Đơn hàng vượt hạn mức tín dụng của đại lý ${dealer.shopName || dealer.name} (vượt ${_outboundFormatVND(projectedDebt - creditLimit)})!</div>` : '<div style="color:#15803d; font-weight:bold; margin-top:4px;">✓ Hợp lệ trong hạn mức tín dụng!</div>'}
 </div>`;
}

function confirmDispatchOrder(code) {
  try {
    _outboundRequire('OPERATIONS_STAFF', 'WAREHOUSE_MANAGER', 'STORE_OWNER');
    const s = ChronoDB.readOutboundState();
    const o = s.orders.find(o => o.code === code);
    if (!o) throw new Error('Không tìm thấy lệnh ' + code);
    if (o.status === 'RESERVED') {
      WarehouseOutbound.startPacking(code).then(() => _renderPackingModal(code));
    } else {
      _renderPackingModal(code);
    }
  } catch (e) {
    if (typeof showToast === 'function') showToast(e.message, 'warning');
    else alert(e.message);
  }
}

function _renderPackingModal(code) {
  const s = ChronoDB.readOutboundState();
  const o = s.orders.find(o => o.code === code);
  if (!o) return;
  const expectedSerials = o.items.flatMap(i => i.reservedSerials || []);
  const scanned = o.scannedSerials || [];
  const allDone = expectedSerials.length > 0 && expectedSerials.every(sn => scanned.includes(sn));
  const manage = _outboundCan('WAREHOUSE_MANAGER', 'STORE_OWNER');

  let html = `<div style="margin-bottom:12px;">
    <b>Đơn vị nhận:</b> ${_outboundEsc(o.dealerName)}<br>
    <b>Tiến độ đối soát Serial:</b> <span class="badge-status">${scanned.length}/${expectedSerials.length} chiếc</span>
  </div>`;

  html += `<h4>Smart Picking List (Chỉ định theo FIFO)</h4>`;
  html += `<table class="outbound-table" style="width:100%; font-size:12px; margin-bottom:12px; border-collapse:collapse;">
    <thead><tr style="background:#f1f5f9; text-align:left;"><th>STT</th><th>Serial</th><th>Mã SKU</th><th>Vị trí kệ</th><th>Trạng thái</th><th>Thao tác</th></tr></thead>
    <tbody>`;
  expectedSerials.forEach((sn, idx) => {
    const x = s.serials.find(x => x.serialNumber === sn) || {};
    const isScanned = scanned.includes(sn);
    html += `<tr style="border-bottom:1px solid #e2e8f0; ${isScanned ? 'background:#f0fdf4;' : ''}">
      <td>${idx + 1}</td>
      <td><b>${_outboundEsc(sn)}</b></td>
      <td>${_outboundEsc(x.sku || '')}</td>
      <td>${_outboundEsc(x.shelfLocation || x.currentLocation || 'Kệ kho')}</td>
      <td>${isScanned ? '<span style="color:#16a34a; font-weight:bold;">✓ Đã quét</span>' : '<span style="color:#64748b;">Chưa quét</span>'}</td>
      <td>${!isScanned ? `<button type="button" class="btn-action-small" onclick="submitScanSerial('${_outboundEsc(code)}', '${_outboundEsc(sn)}')">Quét Serial</button>` : ''}</td>
    </tr>`;
  });
  html += `</tbody></table>`;

  if (!allDone) {
    html += `<div class="form-group" style="display:flex; gap:8px;">
      <input type="text" id="manualSerialInput" class="form-input" placeholder="Quét Camera hoặc nhập Serial..." style="flex:1;" onkeydown="if(event.key==='Enter')submitScanSerial('${_outboundEsc(code)}', this.value)">
      <button type="button" class="btn-primary-action" onclick="submitScanSerial('${_outboundEsc(code)}', document.getElementById('manualSerialInput').value)">Đối soát</button>
    </div>`;
  } else {
    html += `<div style="background:#f0fdf4; border:1px solid #86efac; border-radius:6px; padding:12px; margin-top:12px;">
      <h4 style="color:#166534; margin:0 0 8px;">✓ Đã quét đủ 100% Serial! Sẵn sàng đóng kiện & xuất kho.</h4>
      ${_outboundField('Đơn vị / Người vận chuyển *', 'dispatchCarrier', 'Giao Hàng Hỏa Tốc (ChronoExpress)')}
      ${_outboundField('Mã vận đơn / Số seal niêm phong *', 'dispatchTracking', 'VN-' + Math.floor(100000 + Math.random() * 900000))}
      ${_outboundField('Cước phí giao hàng (VNĐ)', 'dispatchFee', '0', 'number')}
      ${manage ? `<button type="button" data-outbound-submit class="btn-primary-action" style="width:100%; margin-top:8px;" onclick="submitFinalDispatch('${_outboundEsc(code)}')">Xác nhận xuất kho & Trừ tồn (F3.2.10)</button>` : '<p style="color:#991b1b;">Cần tài khoản Thủ kho hoặc Chủ kho để Xác nhận xuất kho vật lý.</p>'}
    </div>`;
  }

  _outboundModal(`Soạn hàng & Quét Serial: ${code}`, html);
}

function submitScanSerial(code, input) {
  if (!input || !input.trim()) return;
  return _outboundAction(async () => {
    await WarehouseOutbound.scan(code, input.trim());
    _renderPackingModal(code);
  }, 'Đã đối soát thành công Serial: ' + input.trim(), () => _renderPackingModal(code));
}

function submitFinalDispatch(code) {
  const carrier = document.getElementById('dispatchCarrier')?.value;
  const tracking = document.getElementById('dispatchTracking')?.value;
  const fee = document.getElementById('dispatchFee')?.value;
  return _outboundAction(async () => {
    return await WarehouseOutbound.complete(code, carrier, tracking, fee);
  }, 'Xác nhận xuất kho thành công!', (dispId) => {
    closeModal('generalDetailModal');
    printDispatchA4(code);
  });
}

function printDispatchA4(code) {
  const s = ChronoDB.readOutboundState();
  const o = s.orders.find(o => o.code === code);
  const d = s.dispatches.find(d => d.orderCode === code) || {};
  if (!o) return;
  const serials = d.serials || (o.items || []).flatMap(i => (i.dispatchedSerials || i.reservedSerials || []).map(sn => {
    const x = s.serials.find(x => x.serialNumber === sn) || {};
    return { serialNumber: sn, sku: x.sku || i.sku, watchName: i.name, sourceLocation: x.shelfLocation || 'Kệ kho', unitCost: x.costPrice || x.unitCost || 0 };
  }));

  const itemRows = (o.items || []).map(i => `<tr>
    <td style="border:1px solid #cbd5e1; padding:8px;">${_outboundEsc(i.sku)}</td>
    <td style="border:1px solid #cbd5e1; padding:8px;">${_outboundEsc(i.name)}</td>
    <td style="border:1px solid #cbd5e1; padding:8px; text-align:center;">${i.quantity} ${i.unit === 'BOX' ? 'thùng' : 'chiếc'}</td>
    <td style="border:1px solid #cbd5e1; padding:8px; text-align:center;"><b>${i.convertedQty || i.quantity}</b></td>
  </tr>`).join('');

  const serialRows = serials.map((sn, idx) => `<tr>
    <td style="border:1px solid #cbd5e1; padding:6px; text-align:center;">${idx + 1}</td>
    <td style="border:1px solid #cbd5e1; padding:6px;">${_outboundEsc(sn.sku)}</td>
    <td style="border:1px solid #cbd5e1; padding:6px;"><b>${_outboundEsc(sn.serialNumber)}</b></td>
    <td style="border:1px solid #cbd5e1; padding:6px;">${_outboundEsc(sn.sourceLocation || 'Kệ kho')}</td>
    <td style="border:1px solid #cbd5e1; padding:6px; text-align:right;">${_outboundFormatVND(sn.unitCost)}</td>
  </tr>`).join('');

  const html = `<div id="printA4Content" style="font-family:sans-serif; color:#0f172a; line-height:1.5; padding:20px; background:#fff; border:1px solid #e2e8f0; border-radius:8px;">
    <div style="display:flex; justify-content:space-between; border-bottom:2px solid #0f172a; padding-bottom:8px; margin-bottom:12px;">
      <div>
        <h3 style="margin:0; font-size:16px;">CHRONOVAULT WMS — HỆ THỐNG QUẢN LÝ TỔNG KHO ĐỒNG HỒ</h3>
        <p style="margin:2px 0 0; font-size:12px; color:#475569;">Phân Hệ 3: Đối Tác Đại Lý & Quản Lý Xuất Kho B2B (TV3: Tô Đức Thảo)</p>
      </div>
      <div style="text-align:right; font-size:12px;">
        <b>Mã phiếu: ${d.id || 'PX-' + code}</b><br>
        Lệnh xuất: ${code}
      </div>
    </div>

    <h2 style="text-align:center; margin:16px 0 4px; font-size:18px;">PHIẾU XUẤT KHO KIÊM BIÊN BẢN BÀN GIAO B2B</h2>
    <p style="text-align:center; font-size:12px; color:#64748b; margin:0 0 16px;">Khổ tiêu chuẩn A4 • Lưu vết đối soát 100% Serial Laser</p>

    <div style="display:grid; grid-template-columns:1fr 1fr; gap:12px; font-size:13px; margin-bottom:16px; background:#f8fafc; padding:12px; border-radius:6px;">
      <div>
        <b>Đơn vị tiếp nhận:</b> ${_outboundEsc(o.dealerName)}<br>
        <b>Địa chỉ giao nhận:</b> ${_outboundEsc(d.address || s.dealers.find(x => x.id === o.dealerId)?.address || 'Tại kho')}<br>
        <b>Đơn vị vận chuyển:</b> ${_outboundEsc(d.carrier || 'ChronoExpress')}<br>
        <b>Mã vận đơn / Số seal:</b> ${_outboundEsc(d.trackingNumber || 'CHƯA_CÓ')}
      </div>
      <div>
        <b>Ngày giờ xuất kho:</b> ${_outboundEsc(d.date || o.createdAt || _nowTimestamp())}<br>
        <b>Người lập phiếu:</b> ${_outboundEsc(o.createdByName || o.createdBy || 'Tô Đức Thảo')}<br>
        <b>Người duyệt giữ chỗ:</b> ${_outboundEsc(o.approvedByName || o.approvedBy || 'Võ Công Tâm')}<br>
        <b>Thủ kho thực xuất:</b> ${_outboundEsc(d.dispatchedBy || 'Thủ kho')}
      </div>
    </div>

    <h4 style="margin:12px 0 6px; font-size:14px;">1. Danh mục sản phẩm xuất kho</h4>
    <table style="width:100%; border-collapse:collapse; font-size:12px; margin-bottom:16px;">
      <thead><tr style="background:#f1f5f9;">
        <th style="border:1px solid #cbd5e1; padding:6px; text-align:left;">Mã SKU</th>
        <th style="border:1px solid #cbd5e1; padding:6px; text-align:left;">Tên mẫu đồng hồ</th>
        <th style="border:1px solid #cbd5e1; padding:6px; text-align:center;">Số lượng ĐVT</th>
        <th style="border:1px solid #cbd5e1; padding:6px; text-align:center;">Quy đổi chiếc</th>
      </tr></thead>
      <tbody>${itemRows}</tbody>
    </table>

    <h4 style="margin:12px 0 6px; font-size:14px;">2. Bảng kê chi tiết 100% mã Serial đích danh (${serials.length} chiếc)</h4>
    <table style="width:100%; border-collapse:collapse; font-size:11px; margin-bottom:20px;">
      <thead><tr style="background:#f1f5f9;">
        <th style="border:1px solid #cbd5e1; padding:6px; text-align:center; width:35px;">STT</th>
        <th style="border:1px solid #cbd5e1; padding:6px; text-align:left;">Mã SKU</th>
        <th style="border:1px solid #cbd5e1; padding:6px; text-align:left;">Số Serial Laser</th>
        <th style="border:1px solid #cbd5e1; padding:6px; text-align:left;">Tọa độ kệ rút</th>
        <th style="border:1px solid #cbd5e1; padding:6px; text-align:right;">Giá vốn đích danh</th>
      </tr></thead>
      <tbody>${serialRows}</tbody>
    </table>

    <div style="display:grid; grid-template-columns:repeat(4, 1fr); gap:8px; text-align:center; font-size:12px; margin-top:30px; padding-top:10px;">
      <div><b>Người Lập Phiếu</b><br><small>(Ký & ghi rõ họ tên)</small><br><br><br><br><b>${_outboundEsc(o.createdByName || 'Tô Đức Thảo')}</b></div>
      <div><b>Thủ Kho Xuất Hàng</b><br><small>(Ký & ghi rõ họ tên)</small><br><br><br><br><b>${_outboundEsc(d.dispatchedBy || 'Võ Công Tâm')}</b></div>
      <div><b>Đơn Vị Vận Chuyển</b><br><small>(Ký & ghi rõ họ tên)</small><br><br><br><br><b>${_outboundEsc(d.carrier || 'ChronoExpress')}</b></div>
      <div><b>Đại Lý Nhận Hàng</b><br><small>(Ký & ghi rõ họ tên)</small><br><br><br><br><b>${_outboundEsc(d.receivedBy || o.dealerName)}</b></div>
    </div>
  </div>
  <div style="display:flex; justify-content:flex-end; gap:8px; margin-top:16px;">
    <button type="button" class="btn-toggle-view" onclick="closeModal('generalDetailModal')">Đóng</button>
    <button type="button" class="btn-primary-action" onclick="window.print()">🖨️ In Chứng Từ A4</button>
  </div>`;

  _outboundModal(`Biên bản bàn giao: ${code}`, html);
}

function confirmOutboundHandover(code) {
  try {
    _outboundRequire('WAREHOUSE_MANAGER', 'STORE_OWNER');
    _outboundModal('Xác nhận bàn giao hàng', `
      <p>Nhập người đại diện đại lý ký nhận bàn giao hàng hóa cho lệnh <b>${_outboundEsc(code)}</b>:</p>
      ${_outboundField('Người ký nhận bàn giao *', 'handoverReceiverName', 'Đại diện đại lý')}
      <button type="button" data-outbound-submit class="btn-primary-action" onclick="_submitHandover('${_outboundEsc(code)}')">Xác nhận đã nhận hàng</button>
    `);
  } catch (e) {
    if (typeof showToast === 'function') showToast(e.message, 'warning');
  }
}

function _submitHandover(code) {
  const receiver = document.getElementById('handoverReceiverName')?.value;
  return _outboundAction(() => WarehouseOutbound.handover(code, receiver), 'Đã xác nhận bàn giao hàng hóa thành công.');
}

function openCustomerReturnModal(dealerId) {
  try {
    _outboundRequire('OPERATIONS_STAFF', 'WAREHOUSE_MANAGER', 'STORE_OWNER');
    const s = ChronoDB.readOutboundState();
    const dealers = s.dealers;
    const candidates = s.serials.filter(x => ['DISPATCHED', 'DELIVERED', 'SOLD'].includes(x.status));
    const shelves = ChronoDB.getShelves();

    let html = `<label class="form-group"><span class="form-label">Đơn vị hoàn trả</span>
      <select class="form-select" id="returnDealerSelect">
        ${dealers.map(d => `<option value="${_outboundEsc(d.id)}" ${d.id === dealerId ? 'selected' : ''}>${_outboundEsc(d.shopName || d.name)}</option>`).join('')}
      </select>
    </label>
    <label class="form-group"><span class="form-label">Số Serial hoàn trả (Laser trên hộp) *</span>
      <input class="form-input" id="returnSerialInput" placeholder="VD: OMG-SPEED-2026-001 hoặc chọn bên dưới">
    </label>
    ${candidates.length ? `<p style="font-size:12px; margin:4px 0 8px;">Gợi ý Serial đã xuất gần đây: ${candidates.slice(0, 5).map(c => `<a href="javascript:void(0)" onclick="document.getElementById('returnSerialInput').value='${_outboundEsc(c.serialNumber)}'" style="margin-right:8px; text-decoration:underline;">${_outboundEsc(c.serialNumber)}</a>`).join('')}</p>` : ''}
    <label class="form-group"><span class="form-label">Tình trạng kiểm định chất lượng (F3.1.6)</span>
      <select class="form-select" id="returnConditionSelect" onchange="document.getElementById('returnLocationSelect').value = this.value === 'NEW' ? 'K1-A01-B01' : 'C-01'">
        <option value="NEW">Hàng mới nguyên seal (Đổi mẫu kinh doanh) → Nhập lại Kho Mới</option>
        <option value="DEFECT">Hàng lỗi kỹ thuật / trầy xước → Chuyển Kho Lỗi C-01</option>
      </select>
    </label>
    <label class="form-group"><span class="form-label">Ngăn kệ đích tiếp nhận</span>
      <select class="form-select" id="returnLocationSelect">
        ${shelves.map(sh => `<option value="${_outboundEsc(sh.id)}">${_outboundEsc(sh.name || sh.id)}</option>`).join('')}
      </select>
    </label>
    ${_outboundField('Lý do / Biên bản kiểm định hoàn trả *', 'returnReasonInput', 'Đại lý gửi hoàn trả theo điều khoản hợp đồng')}
    <button type="button" data-outbound-submit class="btn-primary-action" onclick="submitCustomerReturn()">Lập phiếu nhận hoàn trả (F3.1.5)</button>`;

    _outboundModal('Lập phiếu nhận hàng đại lý trả lại', html);
  } catch (e) {
    if (typeof showToast === 'function') showToast(e.message, 'warning');
  }
}

function submitCustomerReturn() {
  const dId = document.getElementById('returnDealerSelect')?.value;
  const sn = document.getElementById('returnSerialInput')?.value;
  const cond = document.getElementById('returnConditionSelect')?.value;
  const loc = document.getElementById('returnLocationSelect')?.value;
  const reason = document.getElementById('returnReasonInput')?.value;
  return _outboundAction(() => WarehouseOutbound.requestReturn(dId, sn, cond, loc, reason), 'Đã lập phiếu hoàn trả.');
}

function approveOutboundReturn(id) {
  return _outboundAction(() => WarehouseOutbound.approveReturn(id), 'Đã duyệt nhận hoàn trả và cập nhật kho.');
}

function openOtherDispatchModal() {
  try {
    _outboundRequire('OPERATIONS_STAFF', 'WAREHOUSE_MANAGER', 'STORE_OWNER');
    const s = ChronoDB.readOutboundState();
    const candidates = s.serials.filter(x => ['DEFECT', 'DEFECTIVE', 'DISPLAY'].includes(x.status) || (x.status === 'IN_STOCK' && x.qualityType === 'DISPLAY'));

    if (!candidates.length) {
      if (typeof showToast === 'function') showToast('Không có Serial hàng lỗi hoặc hàng trưng bày để xuất.', 'info');
      return;
    }

    let html = `<label class="form-group"><span class="form-label">Chọn Serial hàng lỗi / trưng bày</span>
      <select class="form-select" id="otherSerialSelect">
        ${candidates.map(x => `<option value="${_outboundEsc(x.serialNumber)}">${_outboundEsc(x.serialNumber)} · ${_outboundEsc(x.sku)} (${_outboundEsc(x.status)})</option>`).join('')}
      </select>
    </label>
    <label class="form-group"><span class="form-label">Mục đích xuất kho phi thương mại (F3.2.11)</span>
      <select class="form-select" id="otherPurposeSelect">
        <option value="WARRANTY">Xuất chuyển Trung tâm bảo hành hãng (WARRANTY)</option>
        <option value="DISPOSE">Xuất tiêu hủy phế phẩm vỡ hỏng (Cần Chủ kho phê duyệt)</option>
        <option value="LIQUIDATION">Xuất bán thanh lý hàng trưng bày (Kho Display)</option>
      </select>
    </label>
    ${_outboundField('Lý do / Căn cứ kỹ thuật biên bản giám định *', 'otherReasonInput', 'Xuất chuyển bảo hành định kỳ theo quy trình hãng')}
    <button type="button" data-outbound-submit class="btn-primary-action" onclick="submitOtherDispatch()">Lập phiếu xuất khác</button>`;

    _outboundModal('Lập phiếu xuất khác (Bảo hành / Tiêu hủy)', html);
  } catch (e) {
    if (typeof showToast === 'function') showToast(e.message, 'warning');
  }
}

function submitOtherDispatch() {
  const sn = document.getElementById('otherSerialSelect')?.value;
  const pur = document.getElementById('otherPurposeSelect')?.value;
  const reason = document.getElementById('otherReasonInput')?.value;
  return _outboundAction(() => WarehouseOutbound.requestOther(sn, pur, reason), 'Đã lập phiếu xuất khác.');
}

function approveOutboundOther(id) {
  return _outboundAction(() => WarehouseOutbound.approveOther(id), 'Đã duyệt phiếu xuất khác.');
}

function openDealerReceiptModal(dealerId) {
  try {
    _outboundRequire('OPERATIONS_STAFF', 'WAREHOUSE_MANAGER', 'STORE_OWNER');
    const s = ChronoDB.readOutboundState();
    const d = s.dealers.find(d => d.id === dealerId) || s.dealers[0] || {};
    const debt = d.currentDebt || 0;
    const limit = d.creditLimit || 0;

    let html = `<div style="background:#f8fafc; border-radius:6px; padding:12px; margin-bottom:12px; font-size:13px;">
      <b>Đơn vị tiếp nhận:</b> ${_outboundEsc(d.shopName || d.name)} (${_outboundEsc(d.id)})<br>
      <b>Dư nợ hiện tại:</b> <span style="color:#dc2626; font-weight:bold;">${_outboundFormatVND(debt)}</span><br>
      <b>Hạn mức bảo lãnh (Credit Limit):</b> ${_outboundFormatVND(limit)}<br>
      <b>Hạn mức khả dụng còn lại:</b> ${_outboundFormatVND(Math.max(0, limit - debt))}
    </div>
    <label class="form-group"><span class="form-label">Chọn đơn vị đối soát</span>
      <select class="form-select" id="receiptDealerSelect" onchange="openDealerReceiptModal(this.value)">
        ${s.dealers.map(x => `<option value="${_outboundEsc(x.id)}" ${x.id === d.id ? 'selected' : ''}>${_outboundEsc(x.shopName || x.name)} (${_outboundFormatVND(x.currentDebt)})</option>`).join('')}
      </select>
    </label>
    ${_outboundField('Số tiền thu nợ / Giải phóng bảo lãnh (VNĐ) *', 'receiptAmountInput', debt > 0 ? String(Math.min(debt, 500000000)) : '0', 'number')}
    <label class="form-group"><span class="form-label">Phương thức thanh toán</span>
      <select class="form-select" id="receiptMethodSelect">
        <option value="CHUYEN_KHOAN">Chuyển khoản ngân hàng (Ủy nhiệm chi - UNC)</option>
        <option value="TIEN_MAT">Tiền mặt tại quầy kế toán tổng kho</option>
      </select>
    </label>
    ${_outboundField('Chứng từ tham chiếu / Số UNC ngân hàng *', 'receiptDocInput', 'UNC-VCB-' + Math.floor(10000 + Math.random() * 90000))}
    ${_outboundField('Ghi chú phiếu thu', 'receiptNoteInput', 'Giải phóng bảo lãnh & khôi phục hạn mức tín dụng cho đại lý')}
    <button type="button" data-outbound-submit class="btn-primary-action" onclick="submitDealerReceipt('${_outboundEsc(d.id)}')">✓ Lập Phiếu Thu & Khôi Phục Hạn Mức (F3.1.9)</button>`;

    _outboundModal('Lập phiếu Thu nợ đại lý / Thu hồi công nợ', html);
  } catch (e) {
    if (typeof showToast === 'function') showToast(e.message, 'warning');
  }
}

function submitDealerReceipt(dealerId) {
  const amount = Number(document.getElementById('receiptAmountInput')?.value || 0);
  const method = document.getElementById('receiptMethodSelect')?.value || 'CHUYEN_KHOAN';
  const refDoc = document.getElementById('receiptDocInput')?.value || '';
  const note = document.getElementById('receiptNoteInput')?.value || '';

  if (amount <= 0) {
    if (typeof showToast === 'function') showToast('Số tiền thu phải lớn hơn 0.', 'warning');
    return;
  }

  return _outboundAction(() => {
    return WarehouseOutbound.transact(['OPERATIONS_STAFF', 'WAREHOUSE_MANAGER', 'STORE_OWNER'], (s, a) => {
      const d = s.dealers.find(d => d.id === dealerId);
      _outboundAssert(d, 'Không tìm thấy đơn vị nhận.');
      _outboundAssert(amount <= (d.currentDebt || 0), `Số tiền thu (${_outboundFormatVND(amount)}) không được vượt quá dư nợ (${_outboundFormatVND(d.currentDebt)}).`);
      d.currentDebt = Math.max(0, (d.currentDebt || 0) - amount);
      d.availableCredit = Math.min(d.creditLimit || 0, (d.creditLimit || 0) - d.currentDebt);
      const rcptId = _outboundId('PT', s.logs || []);
      _outboundLog(s, a, 'LẬP_PHIẾU_THU_TIỀN_SỈ', `${rcptId}: Thu ${_outboundFormatVND(amount)} từ ${d.shopName || d.name}, dư nợ còn ${_outboundFormatVND(d.currentDebt)}.`);
      return rcptId;
    });
  }, 'Đã lập phiếu thu và khôi phục hạn mức nợ cho đại lý thành công!');
}

function _outboundFormatVND(amount) {
  return Number(amount || 0).toLocaleString('vi-VN') + ' đ';
}
function approveOutboundOrder(code){return _outboundAction(()=>WarehouseOutbound.approve(code),'Đã duyệt và phân bổ Serial.');}
function cancelOutboundOrder(code){_outboundModal('Hủy lệnh xuất',`${_outboundField('Lý do hủy','cancelOutboundReason')}<button data-outbound-submit class="btn-primary-action" data-id="${_outboundEsc(code)}" onclick="submitCancelOutbound(this.dataset.id)">Xác nhận hủy</button>`);}
function submitCancelOutbound(code){return _outboundAction(()=>WarehouseOutbound.cancel(code,document.getElementById('cancelOutboundReason').value),'Đã hủy lệnh và giải phóng giữ chỗ.');}
function viewOrderDetail(code){const o=ChronoDB.getOrders().find(o=>o.code===code);if(!o)return;const d=ChronoDB.getDispatches().find(d=>d.orderCode===code);_outboundModal(`Lệnh ${code}`,`<p>Đơn vị nhận: ${_outboundEsc(o.dealerName)}</p><p>Người lập: ${_outboundEsc(o.createdByName||'Lệnh lịch sử')}<br>Người duyệt: ${_outboundEsc(o.approvedByName||'Chưa ghi nhận')}</p><p>${_outboundEsc(o.note)}</p>${o.items.map(i=>`<h4>${_outboundEsc(i.name||i.sku)} · ${i.convertedQty||i.quantity} chiếc</h4><p>${_outboundEsc((i.dispatchedSerials?.length?i.dispatchedSerials:i.reservedSerials||[]).join(', '))}</p>`).join('')}${d?`<p>Phiếu ${_outboundEsc(d.id)} · Người xuất ${_outboundEsc(d.dispatchedBy)}<br>Ngày xuất ${_outboundEsc(d.date)}<br>Vận chuyển ${_outboundEsc(d.carrier)} · Vận đơn ${_outboundEsc(d.trackingNumber)}</p>${_outboundButton('In phiếu A4','printDispatchA4',code)}`:''}`);}
