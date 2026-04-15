from product_csr.ports.category_repository_port import CategoryRepositoryPort


class CategoryService:
    def __init__(self, repo: CategoryRepositoryPort):
        self.repo = repo

    def get_all_categories(self, owner_id):
        categories = self.repo.get_all(owner_id=owner_id)
        return [category.to_dict() for category in categories]

    def get_category(self, category_id, owner_id):
        category = self.repo.get_by_id(category_id, owner_id=owner_id)
        if not category:
            raise ValueError("category not found")
        return category.to_dict()

    def create_category(self, data, owner_id):
        if not data.get("title"):
            raise ValueError("Title is required")

        existing = self.repo.get_by_title(data["title"], owner_id=owner_id)
        if existing:
            raise ValueError("Category title already exists")

        data["owner_id"] = str(owner_id)
        category = self.repo.create(data)
        return category.to_dict()

    def update_category(self, category_id, data, owner_id):
        category = self.repo.get_by_id(category_id, owner_id=owner_id)
        if not category:
            raise ValueError("category not found")

        if data.get("title"):
            existing = self.repo.get_by_title(data["title"], owner_id=owner_id)
            if existing and str(existing.id) != str(category.id):
                raise ValueError("Category title already exists")

        updated = self.repo.update(category, data)
        return updated.to_dict()

    def delete_category(self, category_id, owner_id):
        category = self.repo.get_by_id(category_id, owner_id=owner_id)
        if not category:
            raise ValueError("category not found")

        self.repo.delete(category)
        return {"message": "category deleted successfully"}

    def create_category_if_not_exists(self, title, owner_id):
        existing = self.repo.get_by_title(title, owner_id=owner_id)
        if existing:
            return existing

        return self.repo.create({
            "title": title,
            "description": "",
            "owner_id": str(owner_id),
        })
