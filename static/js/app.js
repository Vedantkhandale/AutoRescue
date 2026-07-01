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

})
