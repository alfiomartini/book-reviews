addEventListener('DOMContentLoaded', listeners);

function listeners(){
   
  let info_elm = document.querySelector('.info-container');
  let input = document.querySelector('#search-input');

  input.addEventListener('change', search_clean);
  input.addEventListener('keyup', search_clean);
  input.addEventListener('paste', search_clean);

  function search_clean(){
    info_elm.innerHTML = '';
    // remove event listeners
    input.removeEventListener('change', search_clean);
    input.removeEventListener('keyup', search_clean);
    input.removeEventListener('paste', search_clean);
  }
}