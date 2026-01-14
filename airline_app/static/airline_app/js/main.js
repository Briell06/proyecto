// AeroControl - Main JavaScript

// Configure Tailwind CSS
tailwind.config = {
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        dark: {
          50: '#f8fafc',
          100: '#f1f5f9',
          200: '#e2e8f0',
          300: '#cbd5e1',
          400: '#94a3b8',
          500: '#64748b',
          600: '#475569',
          700: '#334155',
          800: '#1e293b',
          900: '#0f172a',
          950: '#020617',
        }
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
      }
    }
  }
};

// Close message alert
function closeMessage(element) {
  element.classList.add('message-fade-out');
  setTimeout(() => {
    element.remove();
  }, 300);
}

// Auto-dismiss messages after 5 seconds
document.addEventListener('DOMContentLoaded', function() {
  const messages = document.querySelectorAll('.alert-message');
  messages.forEach(function(message) {
    setTimeout(function() {
      closeMessage(message);
    }, 5000);
  });

  // Mobile Resources submenu toggle
  const resourcesToggle = document.getElementById('mobile-resources-toggle');
  const resourcesMenu = document.getElementById('mobile-resources-menu');
  const resourcesIcon = document.getElementById('mobile-resources-icon');
  
  if (resourcesToggle && resourcesMenu && resourcesIcon) {
    resourcesToggle.addEventListener('click', function() {
      resourcesMenu.classList.toggle('hidden');
      resourcesIcon.classList.toggle('rotate-180');
    });
  }

  // Mobile Tools submenu toggle
  const toolsToggle = document.getElementById('mobile-tools-toggle');
  const toolsMenu = document.getElementById('mobile-tools-menu');
  const toolsIcon = document.getElementById('mobile-tools-icon');
  
  if (toolsToggle && toolsMenu && toolsIcon) {
    toolsToggle.addEventListener('click', function() {
      toolsMenu.classList.toggle('hidden');
      toolsIcon.classList.toggle('rotate-180');
    });
  }
});
