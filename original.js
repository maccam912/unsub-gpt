(function() {
  function createMaskWithLabel(element, text, color) {
    var rect = element.getBoundingClientRect();
    var mask = document.createElement('div');
    mask.style.position = 'absolute';
    mask.style.left = `${window.scrollX + rect.left}px`;
    mask.style.top = `${window.scrollY + rect.top}px`;
    mask.style.width = `${rect.width}px`;
    mask.style.height = `${rect.height}px`;
    mask.style.backgroundColor = 'white';
    mask.style.color = 'black';
    mask.style.border = `2px solid ${color}`;
    mask.style.fontSize = '12px'; // Start with 12px font size
    mask.style.display = 'flex';
    mask.style.alignItems = 'center';
    mask.style.justifyContent = 'center';
    mask.style.zIndex = '10000';
    mask.className = 'accessibility-mask';
    mask.textContent = text;
    document.body.appendChild(mask);

    // Adjust font size to fit the mask if necessary
    var fontSize = 12;
    while (mask.scrollWidth > rect.width || mask.scrollHeight > rect.height && fontSize > 5) {
      fontSize--;
      mask.style.fontSize = fontSize + 'px';
    }
  }

  function getColorForElement(element) {
    if (element.tagName.toLowerCase() === 'a') {
      return 'red';
    } else if (element.tagName.toLowerCase() === 'button' || element.type === 'button' || element.type === 'submit') {
      return 'blue';
    } else if (element.type === 'text') {
      return 'green';
    } else if (element.type === 'checkbox') {
      return 'purple';
    } else if (element.type === 'radio') {
      return 'orange';
    } else {
      return 'grey'; // Fallback color
    }
  }

  function getAccessibleName(element) {
    return element.getAttribute('aria-label') || element.innerText || element.value || element.id || element.name || 'unnamed';
  }

  // Remove existing masks if any
  var existingMasks = document.querySelectorAll('.accessibility-mask');
  existingMasks.forEach(function(mask) {
    mask.parentNode.removeChild(mask);
  });

  var elements = document.querySelectorAll('input, button, a');
  elements.forEach(function(element) {
    var name = getAccessibleName(element);
    var color = getColorForElement(element);
    createMaskWithLabel(element, name, color);
  });
})();
