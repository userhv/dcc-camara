/// <reference types="cypress" />

describe('new meeting', () => {
    beforeEach(() => {
      cy.exec('python ../backend/db/init_db.py')
    })
  
    it('new meeting', () => {
      const bossUserName = "Chefe"
      cy.visit('http://localhost:4200/login')
      cy.get('#username').type(`${bossUserName}{enter}`)
      cy.get(".role-text").should('include.text', "Chefia")

      cy.get("#create-meetings-modal-button").click()
      cy.get("#create-meetings-modal").should('include.text', 'Cadastrar reunião')

      const date = "10/10/2100"
      cy.get('#meeting-date').type(date)
      cy.get("#create-meetings-submit-button").click()

      const meetingTitle = 'REUNIÃO DE ' + date
      cy.get(".home-agenda").should('include.text', meetingTitle)
      cy.get(".home-agenda").should('include.text', "Adicionar pauta")
      cy.get(".home-agenda").should('include.text', "Nenhuma pauta foi adicionada")

      cy.get("#create-agenda-modal-button").click()
      cy.get("#create-agenda-modal").should('include.text', 'Cadastrar pauta')

      const agendaTitle = "Agenda Teste"
      cy.get("#agenda-title").type(`${agendaTitle}`)
      cy.get("#agenda-files").selectFile('./src/assets/dcc.png')
      cy.get("#create-agenda-submit-button").click()

      cy.get(".home-agenda").should('include.text', agendaTitle)
      cy.get('.home-agenda').should('not.include.text', 'Nenhuma pauta foi adicionada')

      const teacherUserName = "Discente"
      cy.visit('http://localhost:4200/login')
      cy.get('#username').type(`${teacherUserName}{enter}`)
      cy.get(".role-text").should('include.text', "Representante Discente")

      cy.get(".agenda").should('include.text', meetingTitle)
      cy.contains('.meeting-title', meetingTitle).click()

      cy.get(".preferences.dark-red").should('include.text', "Solicitar pauta")
      cy.get(".list").should('include.text', agendaTitle)

      cy.contains('.preferences.dark-red', "Solicitar pauta").click()
      cy.get("#request-agenda-modal").should('include.text', 'Solicitar pauta')
      
      const requestAgendaTitle = "Agenda Solicitada"
      cy.get("#request-agenda-title").type(`${requestAgendaTitle}`)
      cy.get("#request-agenda-files").selectFile('./src/assets/dcc.png')
      cy.get("#request-agenda-submit-button").click()

      cy.get(".agenda").should('include.text', meetingTitle)
      cy.contains('.meeting-title', meetingTitle).click()

      cy.get(".preferences.dark-red").should('include.text', "Solicitar pauta")
      cy.get(".pendint-list").should('include.text', requestAgendaTitle)

      cy.get(".badge.bg-warning").should('include.text', "Pendente")
      cy.get(".d-flex.justify-content-between").should('include.text', "dcc.png")

      cy.visit('http://localhost:4200/login')
      cy.get('#username').type(`${bossUserName}{enter}`)
      cy.get(".role-text").should('include.text', "Chefia")

      cy.get(".agenda").should('include.text', meetingTitle)
      cy.contains('.meeting-title', meetingTitle).click()

      cy.get(".pendint-list").should('include.text', requestAgendaTitle)
      cy.get(".d-flex.justify-content-between").should('include.text', "dcc.png")

      cy.contains('button', "Solicitar documentos").click()
      cy.get("#add-pending-modal").should('include.text', 'Adicionar pendência')

      const pendingComment = "Me envie documento X"
      cy.get("#pending-comment").type(pendingComment)
      cy.get("#add-pending-submit-button").click()

      cy.visit('http://localhost:4200/login')
      cy.get('#username').type(`${teacherUserName}{enter}`)
      cy.get(".role-text").should('include.text', "Representante Discente")

      cy.get(".agenda").should('include.text', meetingTitle)
      cy.contains('.meeting-title', meetingTitle).click()

      cy.get(".preferences.dark-red").should('include.text', "Solicitar pauta")
      cy.get(".pendint-list").should('include.text', requestAgendaTitle)
      cy.get(".badge.bg-warning").should('include.text', "Pendente")
      cy.get(".d-flex.justify-content-between").should('include.text', "dcc.png")
      cy.get(".card-body").should('include.text', pendingComment)
      cy.get('#request-agenda-files_9').selectFile('./src/assets/logo-dcc.png')
      cy.get('.send-another-document').click()

      cy.visit('http://localhost:4200/login')
      cy.get('#username').type(`${bossUserName}{enter}`)
      cy.get(".role-text").should('include.text', "Chefia")

      cy.get(".agenda").should('include.text', meetingTitle)
      cy.contains('.meeting-title', meetingTitle).click()

      cy.get(".pendint-list").should('include.text', requestAgendaTitle)
      cy.get(".d-flex.justify-content-between").should('include.text', "logo-dcc.png")
      cy.contains('button', "Aprovar").click()

      cy.get(".agenda").should('include.text', meetingTitle)
      cy.contains('.meeting-title', meetingTitle).click()

      cy.get(".list").should('include.text', requestAgendaTitle)

      cy.visit('http://localhost:4200/login')
      cy.get('#username').type(`${teacherUserName}{enter}`)
      cy.get(".role-text").should('include.text', "Representante Discente")

      cy.get(".agenda").should('include.text', meetingTitle)
      cy.contains('.meeting-title', meetingTitle).click()

      cy.get(".list").should('include.text', requestAgendaTitle)
    })
  })
  