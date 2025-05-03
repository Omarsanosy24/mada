from faker import Faker

from tests.create_api_key import get_api_key
from authentication.models import User
from rest_framework.authtoken.models import Token

fake = Faker()
email = "email@student.42abudhabi.ae"

def create_user():
    return User.objects.create_user(
        email=email,
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        password="121323456789",
    )

def test_login(client, db):
    create_user()
    api_key = get_api_key()
    rp = client.post(
        '/auth/login/',
        format="json",
        data={
            "email": email,
            "password": "121323456789",
        },
        HTTP_X_API_KEY=api_key,
    )
    assert rp.status_code == 200, rp.data
    assert "password" not in str(rp.data)
    assert "status" in rp.data and "message" in rp.data
    assert "token" in rp.data['data']
    assert Token.objects.get(key=rp.data['data']['token'])
    # for Email Error
    rp_ = client.post(
        '/auth/login/',
        format="json",
        data={
            "email": "emaisl@gmail.com",
            "password": "123456789",
        }
    )
    assert rp_.status_code == 400, rp_.data
    assert "password" not in str(rp_.data)
    assert "status" in rp_.data and "message" in rp_.data
    # For password error
    rp2 = client.post(
        '/auth/login/',
        format="json",
        data={
            "email": email,
            "password": "1234567829",
        }
    )
    assert rp2.status_code == 400, rp2.data
    assert "status" in rp2.data and "message" in rp2.data


def test_get_user_info(client, db):
    test_create_user(client, db)
    rp = client.get(
        '/auth/profile/',
        format="json",
        HTTP_AUTHORIZATION=f"token {TokenWithEx.objects.first()}"
    )
    assert rp.status_code == 200, rp.data
    assert "status" in rp.data and "message" in rp.data


def test_logout(client, db):
    test_create_user(client, db)
    rp = client.post(
        '/auth/logout/',
        format="json",
        HTTP_AUTHORIZATION=f"token {TokenWithEx.objects.first().key}",
        data={
            "token": f"{TokenWithEx.objects.first().key}s"
        }
    )
    assert rp.status_code == 200, rp.data
    assert "status" in rp.data and "message" in rp.data


def test_profile(client, db):
    test_create_user(client, db)
    rp = client.get(
        '/auth/profile/',
        format="json",
        HTTP_AUTHORIZATION=f"token {TokenWithEx.objects.first().key}",
    )
    assert rp.status_code == 200, rp.data
    assert "status" in rp.data and "message" in rp.data


def test_update_profile(client, db):
    test_create_user(client, db)
    rp = client.patch(
        '/auth/profile/',
        format="json",
        HTTP_AUTHORIZATION=f"token {TokenWithEx.objects.first().key}",
        data={
            "kind": "employee",
            "phone": "011001101",
        }
    )
    assert rp.status_code == 200, rp.data
    assert "status" in rp.data and "message" in rp.data


def test_statistics(client, db):
    test_create_user(client, db)

    MealModel.objects.create(
        category=CategoryModel.objects.create(name="test"),
        name="test",
        description="test",
    )
    user = User.objects.first()
    DailyMealyForUserModel.objects.create(
        user=User.objects.first(),
        daily_meal=MealModel.objects.first(),
    )
    rp = client.get(
        '/auth/statistic/',
        format="json",
        HTTP_AUTHORIZATION=get_api_key(),
    )
    assert rp.status_code == 200, rp.data
    assert "status" in rp.data and "message" in rp.data


def test_get_highest_point_users(client, db):
    test_create_user(client, db)
    UserPoints.objects.create(
        user=User.objects.first(),
        points=100,
        kind="add",
    )
    UserPoints.objects.create(
        user=User.objects.first(),
        points=2,
        kind="remove",
    )

    rp = client.get(
        '/auth/user/highest-point-users/',
        format="json",
        HTTP_AUTHORIZATION=get_api_key(),
    )
    assert rp.status_code == 200, rp.data
    assert "status" in rp.data and "message" in rp.data
