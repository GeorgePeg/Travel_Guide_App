"""
    Σχεδιασμός των απαραίτητων μοντέλων
"""

from django.db import models
from django.contrib.auth.models import User

# Κλάσση για τις κατηγορίες ενδιαφέροντος, π.χ. Φαγητό, Αξιοθέατα, Νυχτερινή Ζωή
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Όνομα Κατηγορίας Ενδιαφέροντος")
    slug = models.SlugField(max_length=100, unique=True, help_text="URL friendly όνομα (π.χ. fagito-kai-poto)")
    icon = models.CharField(
        max_length=50,
        blank=True,
        help_text="Εικονίδο από το FontAwesome (π.χ. fa-solid fa-landmark)"
    )
    class Meta:
        verbose_name = "Κατηγορία"
        verbose_name_plural = "Κατηγορίες"
    def __str__(self):
        return self.name
# Κλάσση προορισμών
class Destination(models.Model):
    title = models.CharField(max_length=200, verbose_name="Όνομα πόλης")
    slug = models.SlugField(max_length=200, unique=True, help_text="URL friendly όνομα (π.χ. athens-greece)")
    country = models.CharField(max_length=100, verbose_name="Χώρα")
    description = models.TextField(verbose_name="Περιγραφή / Οδηγός για την πόλη")
    # Εικόνα προορισμού (-> στον φάκελο media/destinations)
    cover_image = models.ImageField(upload_to="destinations/", blank=True, null=True, verbose_name="Εικόνα προορισμού για εξώφυλλο")
    # Συντεταγμένες
    latitude = models.FloatField(blank=True, null=True, verbose_name="Γεωγραφικό Πλάτος")
    longitude = models.FloatField(blank=True, null=True, verbose_name="Γεωγραφικό Μήκος")
    # Ορισμός flag για εμφάνιση του προορισμού στους προτεινόμενους προορισμούς
    is_featured = models.BooleanField(default=False, verbose_name="Προτεινόμενος Προορισμός;")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ημερομηνία Δημιουργίας")

    class Meta:
        verbose_name = "Προορισμός"
        verbose_name_plural = "Προοορισμοί"
    def __str__(self):
        return f"{self.title}, {self.country}"
# Κλάσση για τα αξιοθέατα
class PointsOfInterest(models.Model):
    # 1-N -> Πολλά αξιοθέατα ανήκουν σε έναν προορισμό
    destination = models.ForeignKey(
        Destination,
        # Αν η πόλη διαγραφεί τότε να διαγραφθούν και όλα τα αξιοθέατά της
        on_delete=models.CASCADE,
        related_name="pois",
        verbose_name="Προορισμός"
    )
    # Μ-Ν -> Ένα αξιοθέατο μπορεί να ανήκει σε πολλές κατηγορίες
    categories = models.ManyToManyField(Category, related_name="pois", verbose_name="Κατηγορίες")
    title = models.CharField(max_length=200, verbose_name="Τίτλος Αξιοθέατου")
    description = models.TextField(verbose_name="Περιγραφή Αξιοθέατου")
    address = models.CharField(max_length=255, blank=True, verbose_name="Διεύθυνση")
    latitude = models.FloatField(blank=True, null=True, verbose_name="Γεωγραφικό Πλάτος")
    longitude = models.FloatField(blank=True, null=True, verbose_name="Γεωγραφικό Μήκος")
    image = models.ImageField(upload_to="pois/", blank=True, null=True, verbose_name="Φωτογραφία αξιοθέατου")

    # Εύρος Τιμών 
    PRICE_CHOICES = [
        ('€', 'Budget / Οικονομικό'),
        ('€€', 'Moderate / Μεσαίας Κλίμακας'),
        ('€€€', 'Expensive / Ακριβό'),
        ('€€€€', 'Luxury / Πολύ ακριβό')
    ]
    price_range = models.CharField(
        max_length=10,
        choices=PRICE_CHOICES,
        default='€€',
        verbose_name="Κλίμακα Τιμής"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ημερομηνία Δημιουργίας")
    class Meta:
        verbose_name = "Αξιοθέατο / Σημείο Ενδιαφέροντος"
        verbose_name_plural = "Αξιοθέατα / Σημεία Ενδιαφέροντος"
    def __str__(self):
        return f"{self.title} ({self.destination.title})"
class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookmarks')
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='bookmarked_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'destination') # Αποφεύγουμε διπλότυπα

    def __str__(self):
        return f"{self.user.username} -> Bookmark: {self.destination.title}"
class Visited(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='visited_places')
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='visited_by')
    visited_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'destination') # Αποφεύγουμε διπλότυπα

    def __str__(self):
        return f"{self.user.username} -> Visited: {self.destination.title}"