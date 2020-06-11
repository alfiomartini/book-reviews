addEventListener('DOMContentLoaded', listeners);

function listeners(){
  
  let alert = document.querySelector('.alert');
  let  add_review = document.getElementById('add-review');
  let info_elm = document.querySelector('.info-container');
  let input = document.querySelector('#search-input');
  let  add_container = document.querySelector('.rev-add-container')

  input.addEventListener('change', search_clean);
  input.addEventListener('keyup', search_clean);
  input.addEventListener('paste', search_clean);

  function search_clean(){
    info_elm.style.display = 'none';
    add_container.style.display = 'none';
    add_review.style.display = 'none';
    alert.style.display = 'none';
    // remove event listeners
    input.removeEventListener('change', search_clean);
    input.removeEventListener('keyup', search_clean);
    input.removeEventListener('paste', search_clean);
  }
}