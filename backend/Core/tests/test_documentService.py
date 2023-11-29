import unittest
from unittest.mock import MagicMock, patch
import sys
sys.path.insert(0,"..")
sys.path.insert(0,"../..")
import jwt
from backend.Core.adapters.documentService import *  

class TestdocumentService(unittest.TestCase):
    @patch("jwt.decode")
    def test_createNewDocument_success_Chefia(self,mock_jwt_encode):
        title = "document"
        meetingId =1
        path ="uploads/path"
        reqUserId= 2
        comment = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Curabitur eleifend lectus at nulla placerat, et efficitur ipsum efficitur. Ut egestas suscipit ante nec interdum. Vivamus et nisi ultrices, venenatis metus vitae, "
        mock_jwt_encode.return_value = {"user_type":"Chefia"}
        document = documentSerivce.createNewDocument(secretKey="any",token="any",meetingId=meetingId,title=title,path=path,reqUserId=reqUserId, comment=comment)
        self.assertEqual(document.title,title)
        self.assertEqual(document.meetingId,meetingId)
        self.assertEqual(document.path,path)
        self.assertEqual(document.reqUserId,reqUserId)
        self.assertEqual(document.comment,comment)
        # this is the real test
        # it should be automatically approved bc jwt.encode call was mocked as user_type=chefia
        self.assertEqual(document.approved,True)

    @patch("jwt.decode")
    def test_createNewDocument_success_Discente(self,mock_jwt_encode):
        title = "document"
        meetingId =1
        path ="uploads/path"
        reqUserId= 2
        comment = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Curabitur eleifend lectus at nulla placerat, et efficitur ipsum efficitur. Ut egestas suscipit ante nec interdum. Vivamus et nisi ultrices, venenatis metus vitae, "
        mock_jwt_encode.return_value = {"user_type":"Discente"}
        document = documentSerivce.createNewDocument(secretKey="any",token="any",meetingId=meetingId,title=title,path=path,reqUserId=reqUserId, comment=comment)
        self.assertEqual(document.title,title)
        self.assertEqual(document.meetingId,meetingId)
        self.assertEqual(document.path,path)
        self.assertEqual(document.reqUserId,reqUserId)
        self.assertEqual(document.comment,comment)
        # this is the real test
        # it should be automatically not approved bc jwt.encode call was mocked as user_type=Discente
        self.assertEqual(document.approved,False)
    
   
    def test_getFile_success(self):
        agenda_title = "document"
        reuniao_id ="1"
        reunion_title = "TestTitle"
        agenda_id = "2"
        upload_folder= "upload/path"
        document = "Test "
        documentSerivceInst =documentSerivce()
        fileName=documentSerivceInst.getFile(reunion_title=reunion_title, agenda_title=agenda_title, reuniao_id=reuniao_id, agenda_id=agenda_id, document=document,upload_folder=upload_folder)
        expected = upload_folder+"/"+reunion_title+"_"+reuniao_id+"\\"+agenda_title+"_"+agenda_id+"\\"+document
        self.assertEqual(fileName,expected)

    @patch("jwt.decode")
    @patch("psycopg2.connect")
    def test_getAllAgenda_success(self, mock_connect, mock_jwt_decode):
        # Configuração do mock para jwt.decode
        mock_jwt_decode.return_value = {"user_id": 1}

        # Configuração do mock para psycopg2.connect
        mock_conn = mock_connect.return_value
        mock_cursor = mock_conn.cursor.return_value
        mock_cursor.fetchall.return_value = [("Title 1", 1, "Document 1", True, "Comment 1", 101, "User 1", "2023-01-01")]

        # Configuração do token e chave secreta (não são usados, mas são necessários)
        token = "any_token"
        secret_key = "any_secret"

        # Execução da função a ser testada
        result = documentSerivce.getAllAgenda(token, secret_key, mock_conn)

        # Verificação dos resultados esperados
        expected_result = [["Title 1", 1, "Document 1", True, "Comment 1", 101, "User 1", "2023-01-01"]]
        self.assertEqual(result, expected_result)

    @patch("jwt.decode")
    def test_approveDocument_success_Chefia(self, mock_jwt_decode):
        # Configuração do mock para jwt.decode
        mock_jwt_decode.return_value = {"user_type": "Chefia"}

        # Criação de um objeto Document fictício
        document = MagicMock()
        document.approved = False

        # Configuração do token e chave secreta (não são usados, mas são necessários)
        token = "any_token"
        secret_key = "any_secret"

        # Execução da função a ser testada
        documentSerivce.approveDocument(token, secret_key, document)

        # Verificação se a propriedade 'approved' do documento foi alterada para True
        self.assertTrue(document.approved)

    @patch("jwt.decode")
    def test_approveDocument_failure_Discente(self, mock_jwt_decode):
        # Configuração do mock para jwt.decode
        mock_jwt_decode.return_value = {"user_type": "Discente"}

        # Criação de um objeto Document fictício
        document = MagicMock()
        document.approved = False

        token = "any_token"
        secret_key = "any_secret"

        # Execução da função a ser testada
        documentSerivce.approveDocument(token, secret_key, document)

        self.assertFalse(document.approved)

    @patch("psycopg2.connect")
    def test_getDocuments_success(self, mock_connect):
        # Configuração do mock para psycopg2.connect
        mock_conn = mock_connect.return_value
        mock_cursor = mock_conn.cursor.return_value
        mock_cursor.fetchone.return_value = ("Reunion Title",)

        # Configuração dos parâmetros para a função
        title = "Document Title"
        document = "document.pdf"
        reunion_id = 1
        upload_folder = "/uploads"

        # Criação de um objeto Document fictício
        documentServiceInstance = documentSerivce()
        documentServiceInstance.getFile = MagicMock(return_value="/uploads/Reunion_Title_1/Document_Title_1/document.pdf")

        # Execução da função a ser testada
        result = documentServiceInstance.getDocuments(title, document, mock_conn, reunion_id, upload_folder)

        # Verificação dos resultados esperados
        expected_result = "/uploads/Reunion_Title_1/Document_Title_1/document.pdf"
        self.assertEqual(result, expected_result)


    @patch("psycopg2.connect")
    def test_getDocuments_failure_no_data(self, mock_connect):
        # Configuração do mock para psycopg2.connect
        mock_conn = mock_connect.return_value
        mock_cursor = mock_conn.cursor.return_value
        mock_cursor.fetchall.return_value = []

        # Configuração dos parâmetros para a função
        title = "Document Title"
        document = "document.pdf"
        reunion_id = 1
        upload_folder = "/uploads"

        # Criação de um objeto Document fictício
        documentServiceInstance = documentSerivce()

        # Execução da função a ser testada
        result = documentServiceInstance.getDocuments(title, document, mock_conn, reunion_id, upload_folder)

        # Verificação dos resultados esperados
        expected_result = ('Agenda não encontrada', 404)
        self.assertEqual(result, expected_result)
    
    def test_allowed_file_valid_extension(self):
        # Configuração dos parâmetros para a função
        filename = "document.pdf"
        allowed_extensions = {"pdf", "txt", "doc"}

        # Execução da função a ser testada
        result = documentSerivce.allowed_file(filename, allowed_extensions)

        # Verificação do resultado esperado
        self.assertTrue(result)

    def test_allowed_file_invalid_extension(self):
        # Configuração dos parâmetros para a função
        filename = "image.jpg"
        allowed_extensions = {"pdf", "txt", "doc"}

        # Execução da função a ser testada
        result = documentSerivce.allowed_file(filename, allowed_extensions)

        # Verificação do resultado esperado
        self.assertFalse(result)

    @patch("psycopg2.connect")
    def test_updateAgendaComment_success(self, mock_connect):
        # Configuração do mock para psycopg2.connect
        mock_conn = mock_connect.return_value
        mock_cursor = mock_conn.cursor.return_value

        # Configuração dos parâmetros para a função
        agenda_id = 1
        comment = "New comment"

        # Execução da função a ser testada
        documentSerivce.updateAgendaComment(agenda_id, comment, mock_conn)

        # Verificação se o método execute foi chamado corretamente
        mock_cursor.execute.assert_called_once_with('UPDATE pauta SET comentario = %s WHERE id = %s', (comment, agenda_id))
        # Verificação se o método commit foi chamado
        mock_conn.commit.assert_called_once()

    @patch("psycopg2.connect")
    def test_approveAgenda_success(self, mock_connect):
        # Configuração do mock para psycopg2.connect
        mock_conn = mock_connect.return_value
        mock_cursor = mock_conn.cursor.return_value

        # Configuração dos parâmetros para a função
        agenda_id = 1

        # Execução da função a ser testada
        documentSerivce.approveAgenda(agenda_id, mock_conn)

        # Verificação se o método execute foi chamado corretamente
        mock_cursor.execute.assert_called_once_with('UPDATE pauta SET aprovado = %s WHERE id = %s', (True, agenda_id))
        # Verificação se o método commit foi chamado
        mock_conn.commit.assert_called_once()
