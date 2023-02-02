(() => {
    const forms = document.querySelectorAll('.form-delete')

    for (const form of forms) {
        form.addEventListener('submit', function(e) {
            e.preventDefault()

            const confirmed = confirm('Are you sure?')

            if (confirmed) {
                form.submit()
            }
        })
    }
})();

// criando um outro escopo que não vai colidir com os que tão de fora
// é uma arrow function, criada e executada ao mesmo tempo

(() => {
    // essas são as 3 coisas que vão participar dessa "engrenagem"
    const buttonCloseMenu = document.querySelector('.button-close-menu')
    const buttonShowMenu = document.querySelector('.button-show-menu')
    const menuContainer = document.querySelector('.menu-container')

    const buttonShowMenuVisibleClass = 'button-show-menu-visible'
    const menuHiddenClass = 'menu-hidden'

    const closeMenu = () => {
        buttonShowMenu.classList.add(buttonShowMenuVisibleClass)
        // menu hidden é quem esconde o menu
        menuContainer.classList.add(menuHiddenClass)
    }

    const showMenu = () => {
        // na parte que estará mostrando o menu, ele removerá o botão com ícone fas fa-bars
        buttonShowMenu.classList.remove(buttonShowMenuVisibleClass)
        // menu hidden é quem esconde o menu
        menuContainer.classList.remove(menuHiddenClass)
    }

    // button close é o ícone de X
    if (buttonCloseMenu) {
        // quando removo e adiciono elementos na tela, pode ser q fique adionando eventlistener a todo momento, portanto antes disso temos que garantir q essa função não está lá utilizando o removeevent
        buttonCloseMenu.removeEventListener('click', closeMenu)
        buttonCloseMenu.addEventListener('click', closeMenu)
    }
    if (buttonShowMenu) {
        buttonCloseMenu.removeEventListener('click', showMenu)
        buttonShowMenu.addEventListener('click', showMenu)
    }
})();
