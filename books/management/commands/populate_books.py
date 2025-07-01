from django.core.management.base import BaseCommand
from books.models import Book, Author, Category
from decimal import Decimal
from datetime import date

class Command(BaseCommand):
    help = 'Populate the database with professional dog books and images'

    def handle(self, *args, **options):
        # Create categories
        categories = {
            'Dog Training': 'Professional training techniques and methods',
            'Puppy Care': 'Everything you need for your new puppy',
            'Dog Behavior': 'Understanding canine psychology and behavior',
            'Dog Breeds': 'Comprehensive guides to different dog breeds',
            'Dog Health': 'Veterinary care and health maintenance',
            'Working Dogs': 'Service dogs, therapy dogs, and working breeds',
            'Dog Stories': 'Heartwarming tales and memoirs',
            'Dog Sports': 'Agility, competitions, and canine athletics'
        }
        
        for cat_name, description in categories.items():
            category, created = Category.objects.get_or_create(
                name=cat_name,
                defaults={'description': description, 'slug': cat_name.lower().replace(' ', '-')}
            )
            if created:
                self.stdout.write(f"Created category: {cat_name}")

        # Create authors
        authors_data = [
            {'name': 'Patricia McConnell', 'bio': 'Certified Applied Animal Behaviorist and internationally renowned expert on dog behavior'},
            {'name': 'Karen Pryor', 'bio': 'Pioneer in positive reinforcement training and clicker training methods'},
            {'name': 'Stanley Coren', 'bio': 'Professor emeritus and expert on dog intelligence and behavior'},
            {'name': 'Sophia Yin', 'bio': 'Veterinarian and animal behaviorist specializing in low-stress handling'},
            {'name': 'Ian Dunbar', 'bio': 'Veterinarian and animal behaviorist, founder of dog-friendly training'},
            {'name': 'Cesar Millan', 'bio': 'Professional dog trainer and television personality'},
            {'name': 'Victoria Stilwell', 'bio': 'Professional dog trainer and positive reinforcement advocate'},
            {'name': 'Turid Rugaas', 'bio': 'Norwegian dog trainer specializing in calming signals'},
        ]

        authors = {}
        for author_data in authors_data:
            author, created = Author.objects.get_or_create(
                name=author_data['name'],
                defaults={'biography': author_data['bio']}
            )
            authors[author_data['name']] = author
            if created:
                self.stdout.write(f"Created author: {author_data['name']}")

        # Professional dog books with real cover images
        books_data = [
            {
                'title': 'The Other End of the Leash',
                'authors': ['Patricia McConnell'],
                'description': 'A revolutionary look at our relationship with dogs that helps us understand how to better communicate with our four-legged friends.',
                'price': Decimal('16.99'),
                'stock': 25,
                'categories': ['Dog Behavior', 'Dog Training'],
                'cover_image': 'https://images-na.ssl-images-amazon.com/images/I/51VQF+XN8JL._SX331_BO1,204,203,200_.jpg',
                'publisher': 'Ballantine Books',
                'published_date': date(2002, 8, 27),
                'page_count': 272,
                'isbn_13': '9780345446794'
            },
            {
                'title': 'Don\'t Shoot the Dog',
                'authors': ['Karen Pryor'],
                'description': 'The classic guide to positive reinforcement training that revolutionized animal training and human behavior modification.',
                'price': Decimal('15.99'),
                'stock': 30,
                'categories': ['Dog Training'],
                'cover_image': 'https://images-na.ssl-images-amazon.com/images/I/51+oQrNDqeL._SX331_BO1,204,203,200_.jpg',
                'publisher': 'Bantam',
                'published_date': date(1999, 6, 1),
                'page_count': 256,
                'isbn_13': '9780553380392'
            },
            {
                'title': 'The Intelligence of Dogs',
                'authors': ['Stanley Coren'],
                'description': 'A comprehensive ranking of dog breeds by intelligence and an exploration of canine mental abilities.',
                'price': Decimal('17.99'),
                'stock': 20,
                'categories': ['Dog Behavior', 'Dog Breeds'],
                'cover_image': 'https://images-na.ssl-images-amazon.com/images/I/51yXvgW7aqL._SX331_BO1,204,203,200_.jpg',
                'publisher': 'Free Press',
                'published_date': date(2006, 8, 8),
                'page_count': 352,
                'isbn_13': '9780743280877'
            },
            {
                'title': 'Perfect Puppy in 7 Days',
                'authors': ['Sophia Yin'],
                'description': 'A veterinarian\'s guide to raising a well-behaved puppy using positive training methods.',
                'price': Decimal('19.99'),
                'stock': 35,
                'categories': ['Puppy Care', 'Dog Training'],
                'cover_image': 'https://images-na.ssl-images-amazon.com/images/I/518HQJ2TPRL._SX331_BO1,204,203,200_.jpg',
                'publisher': 'CattleDog Publishing',
                'published_date': date(2011, 3, 15),
                'page_count': 344,
                'isbn_13': '9780964151871'
            },
            {
                'title': 'Before and After Getting Your Puppy',
                'authors': ['Ian Dunbar'],
                'description': 'The essential guide for puppy socialization and training from one of the world\'s most respected dog trainers.',
                'price': Decimal('14.99'),
                'stock': 40,
                'categories': ['Puppy Care'],
                'cover_image': 'https://images-na.ssl-images-amazon.com/images/I/51fB4rJg3BL._SX331_BO1,204,203,200_.jpg',
                'publisher': 'New World Library',
                'published_date': date(2004, 9, 14),
                'page_count': 256,
                'isbn_13': '9781577314561'
            },
            {
                'title': 'Cesar\'s Way',
                'authors': ['Cesar Millan'],
                'description': 'The natural, everyday guide to understanding and correcting common dog problems.',
                'price': Decimal('16.99'),
                'stock': 22,
                'categories': ['Dog Training', 'Dog Behavior'],
                'cover_image': 'https://images-na.ssl-images-amazon.com/images/I/51TXB8kJ3dL._SX331_BO1,204,203,200_.jpg',
                'publisher': 'Harmony Books',
                'published_date': date(2006, 9, 26),
                'page_count': 320,
                'isbn_13': '9780307337610'
            },
            {
                'title': 'It\'s Me or the Dog',
                'authors': ['Victoria Stilwell'],
                'description': 'How to have the perfect pet with positive training methods that build trust and respect.',
                'price': Decimal('15.99'),
                'stock': 28,
                'categories': ['Dog Training'],
                'cover_image': 'https://images-na.ssl-images-amazon.com/images/I/51Ac4wjRyNL._SX331_BO1,204,203,200_.jpg',
                'publisher': 'Houghton Mifflin Harcourt',
                'published_date': date(2007, 1, 2),
                'page_count': 288,
                'isbn_13': '9780547085913'
            },
            {
                'title': 'On Talking Terms with Dogs: Calming Signals',
                'authors': ['Turid Rugaas'],
                'description': 'Learn to recognize and understand the calming signals dogs use to communicate and avoid conflict.',
                'price': Decimal('12.99'),
                'stock': 18,
                'categories': ['Dog Behavior'],
                'cover_image': 'https://images-na.ssl-images-amazon.com/images/I/41P5Qk5Z+zL._SX331_BO1,204,203,200_.jpg',
                'publisher': 'Dogwise Publishing',
                'published_date': date(2006, 4, 1),
                'page_count': 64,
                'isbn_13': '9781929242818'
            },
            {
                'title': 'The Complete Dog Breed Book',
                'authors': ['DK Publishing'],
                'description': 'A comprehensive guide to over 400 dog breeds with stunning photography and detailed breed profiles.',
                'price': Decimal('29.99'),
                'stock': 15,
                'categories': ['Dog Breeds'],
                'cover_image': 'https://images-na.ssl-images-amazon.com/images/I/61QJ3QdkIkL._SX384_BO1,204,203,200_.jpg',
                'publisher': 'DK',
                'published_date': date(2013, 4, 15),
                'page_count': 360,
                'isbn_13': '9781465408440'
            },
            {
                'title': 'The Art of Raising a Puppy',
                'authors': ['The Monks of New Skete'],
                'description': 'A comprehensive guide to puppy care and training from the renowned dog-training monks.',
                'price': Decimal('18.99'),
                'stock': 32,
                'categories': ['Puppy Care', 'Dog Training'],
                'cover_image': 'https://images-na.ssl-images-amazon.com/images/I/51CZQdqKF8L._SX331_BO1,204,203,200_.jpg',
                'publisher': 'Little Brown and Company',
                'published_date': date(2011, 8, 30),
                'page_count': 352,
                'isbn_13': '9780316083270'
            },
            {
                'title': 'Inside of a Dog',
                'authors': ['Alexandra Horowitz'],
                'description': 'What dogs see, smell, and know - a fascinating exploration of the canine mind.',
                'price': Decimal('16.99'),
                'stock': 24,
                'categories': ['Dog Behavior'],
                'cover_image': 'https://images-na.ssl-images-amazon.com/images/I/51Z8q5B7+IL._SX331_BO1,204,203,200_.jpg',
                'publisher': 'Scribner',
                'published_date': date(2010, 8, 24),
                'page_count': 368,
                'isbn_13': '9781416583431'
            },
            {
                'title': 'The Puppy Primer',
                'authors': ['Patricia McConnell', 'Brenda Scidmore'],
                'description': 'A practical guide to puppy socialization and early training for a well-adjusted adult dog.',
                'price': Decimal('13.99'),
                'stock': 26,
                'categories': ['Puppy Care'],
                'cover_image': 'https://images-na.ssl-images-amazon.com/images/I/51jV8QnS+gL._SX331_BO1,204,203,200_.jpg',
                'publisher': 'McConnell Publishing',
                'published_date': date(2009, 1, 1),
                'page_count': 88,
                'isbn_13': '9781891767067'
            }
        ]

        # Create books
        for book_data in books_data:
            # Check if book already exists
            if Book.objects.filter(title=book_data['title']).exists():
                self.stdout.write(f"Book '{book_data['title']}' already exists, skipping...")
                continue

            book = Book.objects.create(
                title=book_data['title'],
                description=book_data['description'],
                price=book_data['price'],
                stock_quantity=book_data['stock'],
                cover_image=book_data['cover_image'],
                publisher=book_data.get('publisher'),
                published_date=book_data.get('published_date'),
                page_count=book_data.get('page_count'),
                isbn_13=book_data.get('isbn_13'),
                is_featured=True,  # Make all books featured for now
                is_available=True
            )

            # Add authors
            for author_name in book_data['authors']:
                if author_name in authors:
                    book.authors.add(authors[author_name])
                else:
                    # Create author if doesn't exist
                    author, created = Author.objects.get_or_create(name=author_name)
                    book.authors.add(author)

            # Add categories
            for cat_name in book_data['categories']:
                try:
                    category = Category.objects.get(name=cat_name)
                    book.categories.add(category)
                except Category.DoesNotExist:
                    pass

            self.stdout.write(f"Created book: {book_data['title']}")

        self.stdout.write(
            self.style.SUCCESS('Successfully populated database with professional dog books!')
        )
