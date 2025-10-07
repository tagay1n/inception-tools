package com.example.inception.recommenders;

import de.tudarmstadt.ukp.clarin.webanno.model.AnnotationLayer;
import de.tudarmstadt.ukp.clarin.webanno.model.AnnotationFeature;
import de.tudarmstadt.ukp.clarin.webanno.api.annotation.util.WebAnnoCasUtil;
import de.tudarmstadt.ukp.inception.recommendation.api.model.RecommenderContext;
import de.tudarmstadt.ukp.inception.recommendation.api.recommender.RecommendationEngine;
import org.apache.uima.cas.CAS;
import org.apache.uima.cas.text.AnnotationFS;
import org.springframework.stereotype.Component;

import java.util.List;

/**
 * A simple recommender that copies the covered text of each span
 * into the target string feature (e.g. "correction").
 */
@Component("copySpanTextRecommender")
public class CopySpanTextRecommender
    extends RecommendationEngine
{
    public CopySpanTextRecommender(AnnotationLayer aLayer, AnnotationFeature aFeature) {
        super(aLayer, aFeature);
    }

    @Override
    public void train(CAS cas, List<AnnotationFS> annotations, RecommenderContext context)
    {
        // No training required — static rule-based recommender
    }

    @Override
    public void predict(CAS cas, RecommenderContext context)
    {
        // For each annotation of the given layer
        for (AnnotationFS ann : cas.getAnnotationIndex(WebAnnoCasUtil.getType(cas, getLayer().getName()))) {
            String spanText = ann.getCoveredText();
            ann.setStringValue(getFeature(), spanText);
        }
    }
}
