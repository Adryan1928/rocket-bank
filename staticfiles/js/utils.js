export const INPUT_ERROR_NOTIFICATION_STYLE = 'text-xs text-red-500 hidden'
export const INPUT_WARNING_NOTIFICATION_STYLE = 'text-xs text-yellow-500 hidden'
export const INPUT_SUCCESS_NOTIFICATION_STYLE = 'text-xs text-green-500 hidden'

export class Notification {
    constructor(id, message, styleClass=INPUT_ERROR_NOTIFICATION_STYLE, className='error') {
        this.id = id;
        this.message = message;
        this.styleClass = styleClass;
        this.className = className;
    }
  
    create() {
        let notification = document.createElement('span');
        notification.id = this.id;
        notification.innerText = this.message;
        notification.className = this.className + ' ' + this.styleClass;

        return notification;
    }
  
    display(parentElement) {
        if (!document.getElementById(this.id)) {
            let notification = this.create();
            parentElement.insertAdjacentElement('afterend', notification);
        }
    }
  
    hide() {
        let notification = document.getElementById(this.id);
        if (notification) {
            notification.style.display = 'none';
        }
    }
  
    show() {
        let notification = document.getElementById(this.id);
        if (notification) {
            notification.style.display = 'block';
        }
    }
  }
