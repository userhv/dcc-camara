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
        expected = upload_folder+"/"+reunion_title+"_"+reuniao_id+"/"+agenda_title+"_"+agenda_id+"/"+document
        self.assertEqual(fileName,expected)
       