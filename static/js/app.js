document.addEventListener('DOMContentLoaded',function(){

  // Modal handling
  const openModal = () => document.getElementById('modal-backdrop').style.display = 'flex'
  const closeModal = () => document.getElementById('modal-backdrop').style.display = 'none'

  document.querySelectorAll('[data-open-request]').forEach(btn=> btn.addEventListener('click', openModal))
  document.getElementById('modal-close')?.addEventListener('click', closeModal)

  // geolocation autofill
  const latEl = document.getElementById('lat')
  const lngEl = document.getElementById('lng')
  if(navigator.geolocation){
    navigator.geolocation.getCurrentPosition(pos=>{
      if(latEl) latEl.value = pos.coords.latitude
      if(lngEl) lngEl.value = pos.coords.longitude
    })
  }

  // ajax submit for mechanic request
  const form = document.getElementById('request-form')
  if(form){
    form.addEventListener('submit', async function(e){
      e.preventDefault()
      const data = new FormData(form)

      const resp = await fetch(form.action,{
        method:form.method || 'POST',
        body: data
      })

      if(resp.ok){
        // show success
        const msg = document.getElementById('request-msg')
        if(msg){ msg.innerText = 'Mechanic Request Sent Successfully 🚗'; msg.style.color = '#8ff0b8' }
        closeModal()
      } else {
        const msg = document.getElementById('request-msg')
        if(msg){ msg.innerText = 'Failed to send request'; msg.style.color = '#ff9a9a' }
      }
    })
  }

  // Accept request handler (for mechanics)
  document.querySelectorAll('[data-accept-request]').forEach(btn=>{
    btn.addEventListener('click', async function(){
      const id = this.dataset.requestId
      if(!id) return
      this.disabled = true
      const res = await fetch('/accept-request', {
        method: 'POST',
        headers: {'Content-Type':'application/json'},
        body: JSON.stringify({id})
      })
      if(res.ok){
        this.innerText = 'Accepted'
        this.classList.remove('btn')
        this.classList.add('status-pill','status-done')
        showToast('Request accepted')
      } else {
        this.disabled = false
        showToast('Failed to accept', true)
      }
    })
  })

  // simple toast
  const showToast = (text, error=false) => {
    let t = document.getElementById('ar-toast')
    if(!t){
      t = document.createElement('div')
      t.id = 'ar-toast'
      t.style.position = 'fixed'
      t.style.right = '20px'
      t.style.bottom = '100px'
      t.style.padding = '10px 14px'
      t.style.borderRadius = '10px'
      t.style.boxShadow = '0 10px 30px rgba(2,6,23,0.6)'
      t.style.zIndex = 9999
      t.style.color = '#071021'
      t.style.fontWeight = 700
      document.body.appendChild(t)
    }
    t.innerText = text
    t.style.background = error? '#ff8a8a' : 'linear-gradient(45deg,#8ff0b8,#6bd6c8)'
    t.style.opacity = '1'
    setTimeout(()=>{ t.style.transition = 'opacity 400ms'; t.style.opacity = '0' }, 2000)
  }

})
