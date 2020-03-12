from django.test import TestCase
from django.urls import reverse, resolve
from app.views import *
from app.models import *

class TestUrls(TestCase):

    def test_(self):
        url = reverse('redirect')
        self.assertEqual(resolve(url).func, redirect)


    def test_studentview(self):
        url = reverse('studentview')
        self.assertEqual(resolve(url).func, studentview)


    def test_hint(self):
        url = reverse('hint')
        self.assertEqual(resolve(url).func, hint)

    
    def test_update_request(self):
        url = reverse('update_request')
        self.assertEqual(resolve(url).func, update_request)
    

    def test_reset_question(self):
        url = reverse('reset_question')
        self.assertEqual(resolve(url).func, reset_question)


    
    def test_faq(self):
        url = reverse('faq')
        self.assertEqual(resolve(url).func, faq)

    

    def test_contact(self):
        url = reverse('contact')
        self.assertEqual(resolve(url).func, contact)

    

    def test_game_master_page(self):
        url = reverse('game_master_page')
        self.assertEqual(resolve(url).func, game_master_page)

    
    def test_create_route(self):
        url = reverse('create_route')
        self.assertEqual(resolve(url).func, create_route)

    def test_create_game(self):
        url = reverse('create_game')
        self.assertEqual(resolve(url).func, create_game)

    
    def test_set_map_false(self):
        url = reverse('set_map_false')
        self.assertEqual(resolve(url).func, set_map_false)

    
    def test_login_page(self):
        url = reverse('login_page')
        self.assertEqual(resolve(url).func, login_page)


    def test_login_view(self):
        url = reverse('login_view')
        self.assertEqual(resolve(url).func, login_view)


    def test_delete_question(self):
        url = reverse('delete_question')
        self.assertEqual(resolve(url).func, delete_question)

    def test_add_question_existing(self):
        url = reverse('add_question_existing')
        self.assertEqual(resolve(url).func, add_question_existing)

    def test_delete_route(self):
        url = reverse('delete_route')
        self.assertEqual(resolve(url).func, delete_route)

    def test_locations(self):
        url = reverse('locations')
        self.assertEqual(resolve(url).func, locations)

    def test_signUp_page(self):
        url = reverse('signUp_page')
        self.assertEqual(resolve(url).func, signUp_page)


    def test_User(self):
        a = User()
        a.userID = 1
        a.username = "test"
        a.save()

        record = User.objects.get(userID = "1")
        self.assertEqual(a,record)





    def test_Developers(self):
        a = Developers()
        a.devID =1
        a.user_userID_id = 1
        a.save()


        record = Developers.objects.get(devID=1)
        self.assertEqual(a,record)


    def test_GameMaster(self):
        a = gameMaster()
        a.GMID = 1
        a.user_userID_id = 1
        a.save()

        record = gameMaster.objects.get(GMID=1)
        self.assertEqual(a,record)


    def test_Routes(self):
        a = Routes()
        a.routeID = 1
        a.Node = "1"
        a.NodeID = 1
        a.RouteName = "Test"
        a.gameMaster_GMID_id = 1
        a.save()

        record = Routes.objects.get(routeID = 1)
        self.assertEqual(a,record)



    def test_Gamecode(self):
        a = Gamecode()
        a.groupcode = "0002"
        a.questionNum = 1
        a.map = "False"
        a.routeID_id = 1
        a.save()

        record = Gamecode.objects.get(groupcode = "0002")
        self.assertEqual(a,record)


    def test_Questions(self):
        a = Questions()
        a.auto_increment_id = 1
        a.questions = "Test"
        a.answers = "Test"
        a.hints = "Test"
        a.node_num = 1
        a.location = " "
        a.latitude = 1
        a.longtitude = 1
        a.routeID_id_id = 1
        a.save()

        record = Gamecode.objects.get(node_num = 1)
        self.assertEqual(a,record)



    








