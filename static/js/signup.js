import { Notification } from './utils.js';

function maskCPF (id) {
    var cpf = document.getElementById(id);
    var cpfValue = cpf.value.replace(/\D/g, '');

    cpfValue = cpfValue.replace(/(\d{3})(\d{1,3})/, '$1.$2');
    cpfValue = cpfValue.replace(/(\d{3}).(\d{3})(\d{1,3})/, '$1.$2.$3');
    cpfValue = cpfValue.replace(/(\d{3}).(\d{3}).(\d{3})(\d{1,2})/, '$1.$2.$3-$4');
    cpf.value = cpfValue;
}

function validateCPF (id) {
    var cpf = document.getElementById(id);
    var notification = new Notification('error-cpf', 'Digite um CPF válido')

    if (cpf.value.length != 14) {
        notification.display(cpf);
        notification.show();
        cpf.focus();
    } else {
        cpf.style.borderColor = 'green';
        notification.hide();
    }
}

function validateAge(id) {
    var birthDateInput = document.getElementById(id);
    var birthDate = new Date(birthDateInput.value);

    var today = new Date();
    var eighteenYearsAgo = new Date(today.getFullYear() - 18, today.getMonth(), today.getDate());

    var notification = new Notification('error-age', 'Você deve ter mais de 18 anos para se cadastrar')

    if (!birthDateInput.value || birthDate > eighteenYearsAgo) {
        notification.display(birthDateInput);
        notification.show();
        birthDateInput.focus();
    } else {
        notification.hide();
    }
}

const form = document.querySelector('form');
form.addEventListener('submit', (event) => {
    event.preventDefault();
    
    validateCPF('cpf');
    
    validateAge('birth_date');

    setTimeout(() => {
        let visibleErrors = Array.from(document.querySelectorAll('.error')).filter(err => {
            return getComputedStyle(err).display !== 'none'; 
        })

        
        if (visibleErrors.length === 0) {
            document.getElementById('cpf').value = document.getElementById('cpf').value.replace(/\D/g, '');
            form.submit();
        }
    }, 0);
}); 

const inputCPF = document.querySelector('#cpf');
inputCPF.addEventListener('input', () => maskCPF('cpf'));
inputCPF.maxLength = 14;
inputCPF.pattern = '[0-9]{3}.[0-9]{3}.[0-9]{3}-[0-9]{2}';

