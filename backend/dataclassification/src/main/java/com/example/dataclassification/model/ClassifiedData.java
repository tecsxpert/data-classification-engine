package com.example.dataclassification.model;

import jakarta.persistence.*;

@Entity
public class ClassifiedData {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String fileName;
    private String fileType;
    private String classificationLabel;
    private Double confidenceScore;
    private String status;

    public ClassifiedData() {
    }

    public ClassifiedData(String fileName, String fileType,
                          String classificationLabel,
                          Double confidenceScore,
                          String status) {
        this.fileName = fileName;
        this.fileType = fileType;
        this.classificationLabel = classificationLabel;
        this.confidenceScore = confidenceScore;
        this.status = status;
    }

    public Long getId() {
        return id;
    }

    public String getFileName() {
        return fileName;
    }

    public String getFileType() {
        return fileType;
    }

    public String getClassificationLabel() {
        return classificationLabel;
    }

    public Double getConfidenceScore() {
        return confidenceScore;
    }

    public String getStatus() {
        return status;
    }

    public void setFileName(String fileName) {
        this.fileName = fileName;
    }

    public void setFileType(String fileType) {
        this.fileType = fileType;
    }

    public void setClassificationLabel(String classificationLabel) {
        this.classificationLabel = classificationLabel;
    }

    public void setConfidenceScore(Double confidenceScore) {
        this.confidenceScore = confidenceScore;
    }

    public void setStatus(String status) {
        this.status = status;
    }
}