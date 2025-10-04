// CÓDIGO PARA LA PÁGINA DE REGISTRO
const formRegistro = document.getElementById("registroForm");
const clave = document.getElementById("clave");
const clave2 = document.getElementById("clave2");
const error = document.getElementById("error");

if (formRegistro) {
  formRegistro.addEventListener("submit", function(event) {
    event.preventDefault();
    let errores = [];

    // Validaciones de contraseña
    if (clave.value.length < 8) errores.push("• Debe tener al menos 8 caracteres");
    if (!/[A-Z]/.test(clave.value)) errores.push("• Debe contener al menos una letra mayúscula");
    if (!/[0-9]/.test(clave.value)) errores.push("• Debe contener al menos un número");
    if (!/[!@#$%^&*(),.?\":{}|<>]/.test(clave.value)) errores.push("• Debe contener al menos un carácter especial");
    if (clave.value !== clave2.value) errores.push("• Las contraseñas no coinciden");

    if (errores.length > 0) {
      error.style.color = "red";
      error.innerHTML = errores.join("<br>");
      error.style.display = "block";
    } else {
      error.style.color = "green";
      error.innerHTML = "✅ Registro exitoso. Redirigiendo a la página de ingreso...";
      error.style.display = "block";
      setTimeout(() => window.location.href = "/usuarios/ingresa/", 2000);
    }
  });
}

// ------------------------------------------------------------------

// CÓDIGO PARA LA PÁGINA DE RECUPERAR CONTRASEÑA
const formRecuperar = document.getElementById("recuperarForm");
const mensaje = document.getElementById("mensaje");

if (formRecuperar) {
  formRecuperar.addEventListener("submit", function(event) {
    event.preventDefault();
    const correo = document.getElementById("correo").value;

    if (correo) {
      mensaje.style.color = "green";
      mensaje.innerHTML = "✅ Enlace de recuperación enviado a tu correo.";
      mensaje.style.display = "block";
      setTimeout(() => window.location.href = "/usuarios/ingresa/", 2000);
    } else {
      mensaje.style.color = "red";
      mensaje.innerHTML = "⚠️ Por favor ingresa un correo válido.";
      mensaje.style.display = "block";
    }
  });
}

// ------------------------------------------------------------------

// CÓDIGO PARA LA PÁGINA DE MODIFICAR PERFIL
const profileForm = document.getElementById('profile-form');
if (profileForm) {
  const profileError = document.getElementById('profile-error');
  const profileSuccess = document.getElementById('profile-success');

  profileForm.addEventListener('submit', function(e) {
    e.preventDefault();
    const nombre = document.getElementById('nombre').value.trim();
    const correo = document.getElementById('correo').value.trim();
    const nueva = document.getElementById('nueva').value;
    const confirmar = document.getElementById('confirmar').value;

    profileError.style.display = 'none';
    profileSuccess.style.display = 'none';

    if (!nombre || !correo) {
      profileError.textContent = 'Completa los campos obligatorios.';
      profileError.style.display = '';
      return;
    }

    if (nueva || confirmar) {
      if (nueva.length < 6) {
        profileError.textContent = 'La nueva contraseña debe tener al menos 6 caracteres.';
        profileError.style.display = '';
        return;
      }
      if (nueva !== confirmar) {
        profileError.textContent = 'Las contraseñas no coinciden.';
        profileError.style.display = '';
        return;
      }
    }

    profileSuccess.textContent = 'Perfil actualizado correctamente (simulado).';
    profileSuccess.style.display = 'block';
  });
}

// ------------------------------------------------------------------

const adminForm = document.getElementById("adminForm");
if (adminForm) {
  adminForm.addEventListener("submit", function(event) {
    event.preventDefault();
    alert("Has ingresado como administrador");
    window.location.href = "/";
  });
}