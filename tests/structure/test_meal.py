from faker import Faker

fake = Faker()


def test_filter_in_meal(client, db):
    from structure.models import MealModel, CategoryModel
    cat = CategoryModel.objects.create(name=fake.name())
    MealModel.objects.create(name=fake.name(), category=cat)
    rp = client.get(f'/meal/')
    assert rp.status_code == 200, rp.data
    assert "results" in rp.data



