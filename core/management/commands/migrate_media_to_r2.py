import os
from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile


class Command(BaseCommand):
    help = 'Migrate existing media files to Cloudflare R2'

    def handle(self, *args, **options):
        if not settings.USE_S3:
            self.stdout.write(
                self.style.ERROR('USE_S3 is not enabled. Please set USE_S3=True in your environment.')
            )
            return

        media_root = os.path.join(settings.BASE_DIR, 'media')
        
        if not os.path.exists(media_root):
            self.stdout.write(
                self.style.WARNING('No local media directory found.')
            )
            return

        self.stdout.write('Starting media files migration to Cloudflare R2...')
        
        uploaded_count = 0
        error_count = 0
        
        for root, dirs, files in os.walk(media_root):
            for file in files:
                local_file_path = os.path.join(root, file)
                relative_path = os.path.relpath(local_file_path, media_root)
                
                # S3 path should use forward slashes
                s3_path = relative_path.replace('\\', '/')
                
                try:
                    # Check if file already exists in R2
                    if default_storage.exists(s3_path):
                        self.stdout.write(f'Skipping {s3_path} (already exists)')
                        continue
                    
                    # Read local file and upload to R2
                    with open(local_file_path, 'rb') as f:
                        file_content = f.read()
                        default_storage.save(s3_path, ContentFile(file_content))
                    
                    uploaded_count += 1
                    self.stdout.write(f'Uploaded: {s3_path}')
                    
                except Exception as e:
                    error_count += 1
                    self.stdout.write(
                        self.style.ERROR(f'Error uploading {s3_path}: {str(e)}')
                    )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Migration completed! Uploaded: {uploaded_count}, Errors: {error_count}'
            )
        )