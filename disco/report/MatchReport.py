# import packages
import pandas as pd

from disco.report.Report import Report
import disco.logs
logger = disco.logs.get(__name__)

class MatchReport(Report):
    '''
        Simple query using provided match list and files
    '''

    def inspect_text(self, page_text, terms):
        """
        if a match for any of the terms, add
        to collection
        """

        # convert all text to lower case to
        # increase likelihood of match
        page_text_lower = page_text.lower()
        page_text_lower = page_text_lower.replace('\r', '').replace('\n', '')

        payload = [
            # populate with match dicts
        ]

        for term in terms:
            sentences = [sentence + '.' for sentence in page_text_lower.split('.') if term in sentence]
            if len(sentences) > 0:
                logger.info('found "{0}" x{1}'.format(term, len(sentences)))
                for sentence in sentences:
                    payload.append({
                        'term': term,
                        'sentence': sentence
                    })

        return payload


    def inspect_doc(self, file, terms):
        """
            if a match for any of the terms, add
            to collection
        """
        # populate with studies in loop
        reports = []

        # extract text and do the search
        for i, chunk in enumerate(file.content_chunks()):

            study = self.inspect_text(chunk, terms)

            for entry in study:
                # only populate if there is a match
                # otherwise it will be a bunch of
                # empty studies

                # supplement with page
                entry['page'] = i + 1

                reports.append(entry)

        return reports

    def process(self, terms):
        """
        inspect files for terms and package in report
        """
        for entry in self.files:
            try:
                logger.info('file - {0}'.format(entry.path))

                # notional output file path
                path_sentences = self.path.joinpath('{0}.csv'.format(entry.path.stem))
                path_summary = self.path.joinpath('{0}-summary.csv'.format(entry.path.stem))
                logger.info('will save to - {0}'.format(path_sentences.resolve()))

                reports = self.inspect_doc(entry, terms)

                # receiving a list of dicts
                # therefore pandas can package into a useful outcome
                if len(reports) > 0:
                    frame_sentences = pd.DataFrame(reports)

                    frame_sentences = frame_sentences[['page', 'term', 'sentence']]
                    logger.info('saving sentence file to - {0}'.format(path_sentences.resolve()))
                    frame_sentences.to_csv(str(path_sentences.resolve()))
                    
                    frame_summary = frame_sentences.pivot_table(
                        index='page',
                        columns='term',
                        aggfunc='size',
                        fill_value=0
                    )
                    logger.info('saving summary file to - {0}'.format(path_sentences.resolve()))
                    frame_summary.to_csv(str(path_summary.resolve()))


            except Exception as e:
                logger.error(e)