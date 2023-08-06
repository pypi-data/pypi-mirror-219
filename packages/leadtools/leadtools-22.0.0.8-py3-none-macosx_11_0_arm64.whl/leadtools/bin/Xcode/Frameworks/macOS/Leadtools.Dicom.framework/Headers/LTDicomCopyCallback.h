// *************************************************************
// Copyright (c) 1991-2023 LEAD Technologies, Inc.
// All Rights Reserved.
// *************************************************************
//
//  LTDicomCopyCallback.h
//  Leadtools.Dicom
//

#import <Leadtools.Dicom/LTDicomElement.h>

typedef NS_OPTIONS(NSUInteger, LTDicomCopyFlags) {
	LTDicomCopyFlagsNone = 0,
};

typedef BOOL (^LTDicomCopyCallback)(LTDicomElement *element, LTDicomCopyFlags flags);
