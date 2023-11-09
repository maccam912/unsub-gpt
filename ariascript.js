(function(){function createMaskWithLabel(e,t,n){var o=e.getBoundingClientRect(),r=document.createElement('div');r.style.position='absolute',r.style.left=window.scrollX+o.left+'px',r.style.top=window.scrollY+o.top+'px',r.style.width=o.width+'px',r.style.height=o.height+'px',r.style.backgroundColor='white',r.style.color='black',r.style.border='2px solid '+n,r.style.fontSize='12px',r.style.display='flex',r.style.alignItems='center',r.style.justifyContent='center',r.style.zIndex='10000',r.className='accessibility-mask',r.textContent=t,document.body.appendChild(r);for(var d=12;r.scrollWidth>o.width||r.scrollHeight>o.height&&d>5;)d--,r.style.fontSize=d+'px'}function getColorForElement(e){return'a'===e.tagName.toLowerCase()?'red':'button'===e.tagName.toLowerCase()||'button'===e.type||'submit'===e.type?'blue':'text'===e.type?'green':'checkbox'===e.type?'purple':'radio'===e.type?'orange':'grey'}function getAccessibleName(e){return e.getAttribute('aria-label')||e.innerText||e.value||e.id||e.name||'unnamed'}document.querySelectorAll('.accessibility-mask').forEach(function(e){e.parentNode.removeChild(e)});var elements=document.querySelectorAll('input, button, a');elements.forEach(function(e){var t=getAccessibleName(e),n=getColorForElement(e);createMaskWithLabel(e,t,n)})})();
