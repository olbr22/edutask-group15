describe('Add a new task', () => {

    let uid // user id
    let name // name of the user (firstName + ' ' + lastName)
    let email // email of the user

    before(function () {
        // create a fabricated user from a fixture
        cy.fixture('user.json').then((user) => {
            cy.request({
                method: 'POST',
                url: 'http://localhost:5000/users/create',
                form: true,
                body: user
            }).then((response) => {
                uid = response.body._id.$oid
                name = user.firstName + ' ' + user.lastName
                email = user.email
            })
        })
    })

    beforeEach(function () {
        // enter the main main page
        cy.visit('http://localhost:3000')

         // login fabricated user
        cy.contains('div', 'Email Address')
            .find('input[type=text]')
            .type(email)
        // submit the form on this page
        cy.get('form')
            .submit()

        // // Create a task for the user
        // cy.request({
        //     method: 'POST',
        //     url: 'http://localhost:5000/tasks/create',
        //     form: true,
        //     body: {
        //         "title": "Title title",
        //         "description": "Popular Song",
        //         "url": "v=dQw4w9WgXcQ",
        //         "userid": uid,
        //         "todos": "watch video"
        //     }
        // }).then((response) => {
        //     cy.log(response.body)
        // })
    })

    it('confirm current page is "Your tasks" page', () => {
        cy.get('h1')
            .should('contain.text', 'Your tasks, ' + name)
    })

    it('confirm the title input is empty', () => {
        cy.get('input[name=title]')
            .should('be.empty')
    })

    it('confirm "Create new Task" btn is disabled', () => {
        cy.get('input[type=submit]')
            .should('be.disabled')
    })

    it('confirm creating of a to-do item', () => {
        // select the title input field and type in a title
        cy.get('input[name=title]')
            .type('Watch before Monday')
        // select url and type in a url
        cy.get('input[name=url]')
            .type('dQw4w9WgXcQ')

        // submit the form
        cy.get('form')
            .submit()

        // confirm that the task has been added
        cy.get('.container .container-element a .title-overlay')
            .should('contain.text', 'Watch before Monday')
    })

    after(function () {
        // clean up by deleting the user from the database
        cy.request({
            method: 'DELETE',
            url: `http://localhost:5000/users/${uid}`
        }).then((response) => {
            cy.log(response.body)
        })
    })
})
