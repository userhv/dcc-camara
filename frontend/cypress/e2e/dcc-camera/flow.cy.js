/// <reference types="cypress" />

const bossUserName = "Chefe";
const teacherUserName = "Discente";

const date = "10/10/2100";

const agendaTitle = "Agenda Teste";
const requestAgendaTitle = "Agenda Solicitada";

const meetingTitle = 'REUNIÃO DE ' + date

const documentFilePath = './src/assets/dcc.png';
const documentFileName = 'dcc.png'

const additionalDocumentFilePath = './src/assets/logo-dcc.png';

const pendingComment = "Documento X";

describe('dcc camara', () => {
    beforeEach(() => {
      initializeDatabase()
    })

    it('new meeting and pending agenda', () => {
      loginAsUser(bossUserName, "Chefia")
      createMeeting(date)
      verifyMeetingIsCreated(meetingTitle)

      loginAsUser(teacherUserName,  "Representante Discente")
      requestAgenda(meetingTitle, requestAgendaTitle, documentFilePath)
      verifyRequestedAgendaIsCreated(meetingTitle, requestAgendaTitle, documentFileName)

      loginAsUser(bossUserName,  "Chefia")
      addPendingDocument(meetingTitle, requestAgendaTitle, pendingComment)

      loginAsUser(teacherUserName,  "Representante Discente")
      updateDocument(meetingTitle, requestAgendaTitle, additionalDocumentFilePath)

      loginAsUser(bossUserName,  "Chefia")
      approveDocument(meetingTitle, requestAgendaTitle)
      verifyAgendaIsDisplayed(meetingTitle, requestAgendaTitle)

      loginAsUser(teacherUserName,  "Representante Discente")
      verifyAgendaIsDisplayed(meetingTitle, requestAgendaTitle)
    })

    it('new meeting and agenda / delete meeting and agenda', () => {
      loginAsUser(bossUserName, "Chefia")
      createMeeting(date)
      verifyMeetingIsCreated(meetingTitle)
      addAgenda(agendaTitle, documentFilePath)

      loginAsUser(teacherUserName,  "Representante Discente")
      verifyAgendaIsDisplayed(meetingTitle, agendaTitle)

      loginAsUser(bossUserName, "Chefia")
      viewMeetingDetails(meetingTitle)
      deleteAgenda(agendaTitle)
      deleteMeeeting(meetingTitle)
    })
  }
)
  
function initializeDatabase() {
  cy.exec('python ../backend/db/init_db.py');
}

function loginAsUser(username, roleText) {
  cy.visit('http://localhost:4200/login');
  cy.get('#username').type(`${username}{enter}`);
  cy.get(".role-text").should('include.text', roleText);
}

function createMeeting(date) {
  cy.get("#create-meetings-modal-button").click()
  cy.get("#create-meetings-modal").should('include.text', 'Cadastrar reunião')

  cy.get("#meeting-date").type(date);
  cy.get("#create-meetings-submit-button").click();
}

function verifyMeetingIsCreated(meetingTitle) {
  cy.get(".home-agenda").should('include.text', meetingTitle)
  cy.get(".home-agenda").should('include.text', "Adicionar pauta")
  cy.get(".home-agenda").should('include.text', "Nenhuma pauta foi adicionada")
}

function addAgenda(agendaTitle, filePath) {
  cy.get("#create-agenda-modal-button").click();
  cy.get("#create-agenda-modal").should('include.text', 'Cadastrar pauta')

  cy.get("#agenda-title").type(`${agendaTitle}`);
  cy.get("#agenda-files").selectFile(filePath);
  cy.get("#create-agenda-submit-button").click();

  cy.get(".home-agenda").should('include.text', agendaTitle)
  cy.get('.home-agenda').should('not.include.text', 'Nenhuma pauta foi adicionada')
}

function verifyAgendaIsDisplayed(meetingTitle, requestAgendaTitle){
  cy.get(".agenda").should('include.text', meetingTitle)
  cy.contains('.meeting-title', meetingTitle).click()

  cy.get(".list").should('include.text', requestAgendaTitle)
}

function requestAgenda(meetingTitle, requestAgendaTitle, filePath) {
  cy.get(".agenda").should('include.text', meetingTitle);
  cy.contains('.meeting-title', meetingTitle).click();

  cy.get(".preferences.dark-red").should('include.text', "Solicitar pauta")

  cy.contains('.preferences.dark-red', "Solicitar pauta").click();
  cy.get("#request-agenda-modal").should('include.text', 'Solicitar pauta')

  cy.get("#request-agenda-title").type(`${requestAgendaTitle}`);
  cy.get("#request-agenda-files").selectFile(filePath);
  cy.get("#request-agenda-submit-button").click();
}

function verifyRequestedAgendaIsCreated(meetingTitle, requestAgendaTitle, fileName) {
  cy.get(".agenda").should('include.text', meetingTitle)
  cy.contains('.meeting-title', meetingTitle).click()

  cy.get(".preferences.dark-red").should('include.text', "Solicitar pauta")
  cy.get(".pendint-list").should('include.text', requestAgendaTitle)

  cy.get(".badge.bg-warning").should('include.text', "Pendente")
  cy.get(".d-flex.justify-content-between").should('include.text', fileName)
}

function addPendingDocument(meetingTitle, requestAgendaTitle, comment) {
  cy.get(".agenda").should('include.text', meetingTitle);
  cy.contains('.meeting-title', meetingTitle).click();

  cy.get(".pendint-list").should('include.text', requestAgendaTitle);

  cy.contains('button', "Solicitar documentos").click();
  cy.get("#add-pending-modal").should('include.text', 'Adicionar pendência');

  cy.get("#pending-comment").type(comment);
  cy.get("#add-pending-submit-button").click();
}

function updateDocument(meetingTitle, requestAgendaTitle, filePath){
  cy.get(".agenda").should('include.text', meetingTitle)
  cy.contains('.meeting-title', meetingTitle).click()

  cy.get(".preferences.dark-red").should('include.text', "Solicitar pauta")
  cy.get(".pendint-list").should('include.text', requestAgendaTitle)
  cy.get(".badge.bg-warning").should('include.text', "Pendente")
  cy.get(".card-body").should('include.text', pendingComment)
  cy.get('#request-agenda-files_8').selectFile(filePath)
  cy.get('.send-another-document').click()
}

function approveDocument(meetingTitle, requestAgendaTitle) {
  cy.get(".agenda").should('include.text', meetingTitle)
  cy.contains('.meeting-title', meetingTitle).click()

  cy.get(".pendint-list").should('include.text', requestAgendaTitle)
  cy.get(".d-flex.justify-content-between").should('include.text', "logo-dcc.png")
  cy.contains('button', "Aprovar").click()
}
  
function viewMeetingDetails(meetingTitle){
  cy.get(".agenda").should('include.text', meetingTitle);
  cy.contains('.meeting-title', meetingTitle).click();

  cy.get(".preferences.dark-red").should('include.text', "Preferências")

  cy.contains('.preferences.dark-red', "Preferências").click();
  cy.get(".meeting-header").should('include.text', meetingTitle)
}

function deleteMeeeting(meetingTitle){
  cy.get(".meeting-header").should('include.text', meetingTitle)
  //cy.get(".delete-meeting").click()
}

function deleteAgenda(agendaTitle){
  cy.get(".list").should('include.text', agendaTitle)
  cy.get(".delete-agenda").click()
  cy.get(".app-content").should('not.include.text', agendaTitle)
  cy.get(".home-agenda").should('include.text', "Nenhuma pauta foi adicionada")
}