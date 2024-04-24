describe('Test: todo', () => {
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
        
        //Click on Task
        cy.get('.title-overlay').click()
    })

    it('1.1: Confirm the Title input is empty.', () => {
        cy.get('.popup input[type=text]')
            .should('be.empty')
    })

    it('2.1: Confirm "Create new Task" button is disabled.', () => {
        cy.get('.popup input[type=submit]')
            .should('be.disabled')
    })

    // it('2.2: Add new to-do item.', () => {
    //     cy.get('input[type=text]')
    //         .type('Watch this week')
    //     cy.get('input[type=submit]').click()

    //     cy.get('span.editable')
    //         .contains('Watch this week')
    //         .should('be.visible');
    // })

    it('2.2: Confirm "Add" button is enabled when "Add a new todo" item is not empty', () => {
        cy.get('.inline-form input[type=text]')
            .type('Watch this video later')
        cy.get('input[type=submit]')
            .should('be.enabled')
    })

    it('2.3: Confirm new (active) to-do item with the given description is appended to the bottom of the list of existing to-do items', () => {
        cy.get('.inline-form input[type=text]')
            .type('Watch this video later')
        cy.get('.inline-form input[type=submit]')
            .click()
        cy.get('li.todo-item .editable')
            .last()
            .contains('Watch this video later')
            .should('be.visible')
    })

    it('3.1: Icon in front of todo is clicked when it was active', () => {
        cy.get('li.todo-item span.checker.unchecked').first().click()

        cy.get('li.todo-item span.checker.checked').first().should('exist');
        // cy.get('li.todo-item span.editable').first().should('have.css', 'text-decoration', 'line-through');

        cy.get('li.todo-item span.editable').first().should(($element) => {
            const textDecoration = $element.css('text-decoration')
            expect(textDecoration).to.include('line-through')
        })
    })

    // it('3.1: Icon in front of todo is clicked when it was active', () => {
    //     cy.get('.checker.unchecked').first().click()

    //     cy.get('.checker.checked').first().should('exist');
    //     cy.get('.editable').first().should('have.css', 'text-decoration', 'line-through');
    // })

    // it('3.1: Icon in front of todo is clicked when it was active', () => {
    //     // cy.get('.inline-form input[type=text]')
    //     //     .type('Watch this video later')
    //     // cy.get('.inline-form input[type=submit]')
    //     //     .click()

    //     cy.get('li.todo-item span.checker.unchecked')
    //         .click()
    //     cy.get('li.todo-item span.editable')
    //         .should(($element) => {
    //         const textDecoration = $element.css('text-decoration')
    //         expect(textDecoration).to.include('line-through')
    //         })
    //     cy.get('li.todo-item span.checker.checked').should('exist');
    // })

    it('3.2: Icon in front of todo is clicked when it was done', () => {
        cy.get('.checker.unchecked').click()
        cy.get('.checker.checked').click()

        cy.get('.checker.unchecked').should('exist');
        // cy.get('.editable').should('have.css', 'text-decoration', 'none');

        cy.get('li.todo-item span.editable').first().should(($element) => {
            const textDecoration = $element.css('text-decoration')
            expect(textDecoration).to.include('none')
        })
    })

    it('4.1: Confirm that todo item is removed when deleted.', () => {
        cy.get('.remover').first().click()
        cy.contains('div', 'watch video')
            .should('not.exist')
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
