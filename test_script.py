try:

    # import packages
    from disco.report.MatchReport import MatchReport
    from disco.batch.Batch import Batch

    batch = Batch()
    batch.add_folder('.', file_pdf=True)

    report = MatchReport(batch.files, './output')

    # define keyterms
    terms = ["environment", "growth", "vegetation"]

    report.process(terms)

except Exception as e:
        print(e)