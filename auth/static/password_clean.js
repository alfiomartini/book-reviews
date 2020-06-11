addEventListener('DOMContentLoaded', listeners);

function listeners(){
   
   
  let input = document.querySelector('#search-input');
  let button = document.getElementById('btn-chg');

  input.addEventListener('change', search_clean);
  input.addEventListener('keyup', search_clean);
  input.addEventListener('paste', search_clean);

  function search_clean(){
    button.style.display = 'none';
    // remove event listeners
    input.removeEventListener('change', search_clean);
    input.removeEventListener('keyup', search_clean);
    input.removeEventListener('paste', search_clean);
  }
}