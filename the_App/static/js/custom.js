// Sidenav
document.addEventListener('DOMContentLoaded', function() {
  var elems = document.querySelectorAll('.sidenav');
  var instances = M.Sidenav.init(elems, {});
});

// Form
document.addEventListener('DOMContentLoaded', function() {
  var elems = document.querySelectorAll('select');
  var instances = M.FormSelect.init(elems, {});
});

// Material Box
document.addEventListener('DOMContentLoaded', function() {
    var elems = document.querySelectorAll('.materialboxed');
    var instances = M.Materialbox.init(elems, {});
  });

// Collapsible
document.addEventListener('DOMContentLoaded', function() {
    var elems = document.querySelectorAll('.collapsible');
    var instances = M.Collapsible.init(elems, {});
  });

// FILE INPUT SECTION
let rfile = document.getElementById('real-file')
let btn = document.getElementById('custom-button')
let span = document.getElementById('custom-text')


// // select the objects
// let image = document.querySelector('.file-field')
// image.firstElementChild.setAttribute('hidden', 'hidden')
// img_inp = image.lastElementChild
//
// // Create a new div for materialize
// let btnDiv = document.createElement('div')
// btnDiv.className = 'btn'
// let span = document.createElement('span')
// span.innerHTML = 'File'
// let input = document.createElement('input')
// input.setAttribute('type', 'file')
// btnDiv.appendChild(span)
// btnDiv.appendChild(input)
//
// let filePathWrapper = document.createElement('div')
// filePathWrapper.className = 'file-path-wrapper'
// filePathWrapper.appendChild(img_inp)
//
//
//
// image.appendChild(btnDiv)
// image.appendChild(filePathWrapper)
// console.log(btnDiv);
