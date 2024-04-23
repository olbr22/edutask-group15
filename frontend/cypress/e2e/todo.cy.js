describe('add a new to-do item', () => {
    // define variables that we need on multiple occasions
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

                let data = {
                    title: "Test Title",
                    description: "Popular Song",
                    url: "dQw4w9WgXcQ",
                    userid: uid,
                    todos: "watch video"
                };

                cy.request({
                    method: 'POST',
                    url: 'http://localhost:5000/tasks/create',
                    form: true,
                    body: data
                })
            })
        })
    })

    beforeEach(function () {
        // enter the main main page
        cy.visit('http://localhost:3000')
        // Login
        cy.contains('div', 'Email Address')
            .find('input[type=text]')
            .type(email)

        cy.get('form')
            .submit()
        // Should now be successfully logged in
        
        cy.get('.title-overlay').click()
    })

    it('login to the system with an existing account', () => {
        // assert that the user is now logged in
        cy.get('h1')
            .should('contain.text', 'Your tasks, ' + name)
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
