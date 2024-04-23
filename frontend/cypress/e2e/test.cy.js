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

        // create a fabricated task
        let task = {
            "title": "Test Title",
            "url": "dQw4w9WgXcQ",
            "userid": uid
        }
        cy.request({
            method: 'POST',
            url: 'http://localhost:5000/tasks/create',
            form: true,
            body: task
        }).then((response) => {
            cy.log(response.body)
        })
    })

    it('confirm current page is task page', () => {
        cy.get('h1')
            .should('contain.text', 'Your tasks, ' + name)
    })
})
