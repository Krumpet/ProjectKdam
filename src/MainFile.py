from CourseDownloaderUpdater import CourseDownloaderUpdater
from PdfToDataParser import PdfToDataParser, pdfFilename

if __name__ == '__main__':
    parser = PdfToDataParser()
    courses, faculties = parser.get_databases_from_pdf(pdf_filename=pdfFilename)
    # TODO: maybe save to files
    downloader = CourseDownloaderUpdater(courses=courses, faculties=faculties)
    downloader.download_and_update_courses()
