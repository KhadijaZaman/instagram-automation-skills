import { workflow, node, trigger, sticky, newCredential, ifElse, switchCase, splitInBatches, nextBatch, expr } from '@n8n/workflow-sdk';

const everyFifteen = trigger({
  type: 'n8n-nodes-base.scheduleTrigger',
  version: 1.4,
  config: {
    name: 'Every 15 minutes',
    parameters: { rule: { interval: [{ field: 'minutes', minutesInterval: 15 }] } }
  },
  output: [{ timestamp: '2026-10-28T19:30:00+05:00' }]
});

const readPosts = node({
  type: 'n8n-nodes-base.googleSheets',
  version: 4.7,
  config: {
    name: 'Read Posts tab',
    parameters: {
      resource: 'sheet',
      operation: 'read',
      authentication: 'oAuth2',
      documentId: { __rl: true, mode: 'id', value: "1ARiXXigTeGEHhrLYptkGRec0JJAmgDw165fMRLeKjeA" },
      sheetName: { __rl: true, mode: 'name', value: 'Posts' },
      options: { outputFormatting: { values: { general: 'FORMATTED_VALUE', date: 'FORMATTED_STRING' } } }
    },
    credentials: { googleSheetsOAuth2Api: newCredential('Google Sheets (Instagram calendar)') }
  },
  output: [{ row_number: 2, id: '2026-10-28-carousel', date: '2026-10-28', time: '19:30', format: 'CAROUSEL', caption: 'Caption text', media_urls: 'https://res.cloudinary.com/x/1.png, https://res.cloudinary.com/x/2.png', status: 'approved' }]
});

const keepDuePosts = node({
  type: 'n8n-nodes-base.filter',
  version: 2.3,
  config: {
    name: 'Keep approved posts that are due',
    parameters: {
      conditions: {
        options: { caseSensitive: false, leftValue: '', typeValidation: 'loose' },
        conditions: [
          { leftValue: expr('{{ String($json.status || "").trim().toLowerCase() }}'), operator: { type: 'string', operation: 'equals' }, rightValue: 'approved' },
          { leftValue: expr('{{ String($json.media_urls || "").trim() }}'), operator: { type: 'string', operation: 'notEmpty', singleValue: true }, rightValue: '' },
          { leftValue: expr("{{ (() => { const t = String($json.time || '00:00').trim(); const tt = t.length < 5 ? t.padStart(5, '0') : t; const d = DateTime.fromISO(String($json.date || '').trim() + 'T' + tt, { zone: 'Asia/Karachi' }); return d.isValid && d.toMillis() <= $now.toMillis(); })() }}"), operator: { type: 'boolean', operation: 'true', singleValue: true }, rightValue: '' }
        ],
        combinator: 'and'
      },
      looseTypeValidation: true
    }
  },
  output: [{ row_number: 2, id: '2026-10-28-carousel', date: '2026-10-28', time: '19:30', format: 'CAROUSEL', caption: 'Caption text', media_urls: 'https://res.cloudinary.com/x/1.png, https://res.cloudinary.com/x/2.png', status: 'approved' }]
});

const loopPosts = splitInBatches({ version: 3, config: { name: 'One post at a time', parameters: { batchSize: 1 } } });

const preparePost = node({
  type: 'n8n-nodes-base.set',
  version: 3.5,
  config: {
    name: 'Prepare post',
    parameters: {
      mode: 'manual',
      includeOtherFields: false,
      assignments: {
        assignments: [
          { id: 'row-id', name: 'row_id', value: expr('{{ String($json.id) }}'), type: 'string' },
          { id: 'format', name: 'format', value: expr('{{ String($json.format || "").trim().toUpperCase() }}'), type: 'string' },
          { id: 'caption', name: 'caption', value: expr('{{ $json.caption || "" }}'), type: 'string' },
          { id: 'urls', name: 'urls', value: expr('{{ String($json.media_urls || "").split(",").map(u => u.trim()).filter(Boolean) }}'), type: 'array' },
          { id: 'started', name: 'started_ms', value: expr('{{ $now.toMillis() }}'), type: 'number' }
        ]
      }
    }
  },
  output: [{ row_id: '2026-10-28-carousel', format: 'CAROUSEL', caption: 'Caption text', urls: ['https://res.cloudinary.com/x/1.png', 'https://res.cloudinary.com/x/2.png'], started_ms: 1793200000000 }]
});

const routeByFormat = switchCase({
  version: 3.4,
  config: {
    name: 'Route by format',
    parameters: {
      mode: 'rules',
      rules: {
        values: [
          { renameOutput: true, outputKey: 'IMAGE', conditions: { options: { caseSensitive: false, leftValue: '', typeValidation: 'strict' }, conditions: [{ leftValue: expr('{{ $json.format }}'), operator: { type: 'string', operation: 'equals' }, rightValue: 'IMAGE' }], combinator: 'and' } },
          { renameOutput: true, outputKey: 'CAROUSEL', conditions: { options: { caseSensitive: false, leftValue: '', typeValidation: 'strict' }, conditions: [{ leftValue: expr('{{ $json.format }}'), operator: { type: 'string', operation: 'equals' }, rightValue: 'CAROUSEL' }], combinator: 'and' } },
          { renameOutput: true, outputKey: 'REEL', conditions: { options: { caseSensitive: false, leftValue: '', typeValidation: 'strict' }, conditions: [{ leftValue: expr('{{ $json.format }}'), operator: { type: 'string', operation: 'equals' }, rightValue: 'REEL' }], combinator: 'and' } }
        ]
      },
      options: { fallbackOutput: 'extra', renameFallbackOutput: 'Unknown format' }
    }
  }
});

const createImage = node({
  type: 'n8n-nodes-base.httpRequest',
  version: 4.5,
  config: {
    name: 'Create image container',
    onError: 'continueErrorOutput',
    parameters: {
      method: 'POST',
      url: "https://graph.instagram.com/v23.0/me/media",
      authentication: 'genericCredentialType',
      genericAuthType: 'httpTemplatedCustomAuth',
      sendBody: true,
      contentType: 'form-urlencoded',
      bodyParameters: { parameters: [{ name: 'image_url', value: expr('{{ $json.urls[0] }}') }, { name: 'caption', value: expr('{{ $json.caption }}') }] }
    },
    credentials: { httpTemplatedCustomAuth: newCredential('Instagram token') }
  },
  output: [{ id: '17900000000000001' }]
});

const splitImages = node({
  type: 'n8n-nodes-base.splitOut',
  version: 1.1,
  config: {
    name: 'One item per carousel image',
    parameters: { fieldToSplitOut: 'urls', include: 'noOtherFields', options: { destinationFieldName: 'image_url' } }
  },
  output: [{ image_url: 'https://res.cloudinary.com/x/1.png' }]
});

const createChild = node({
  type: 'n8n-nodes-base.httpRequest',
  version: 4.5,
  config: {
    name: 'Create carousel image container',
    onError: 'continueRegularOutput',
    parameters: {
      method: 'POST',
      url: "https://graph.instagram.com/v23.0/me/media",
      authentication: 'genericCredentialType',
      genericAuthType: 'httpTemplatedCustomAuth',
      sendBody: true,
      contentType: 'form-urlencoded',
      bodyParameters: { parameters: [{ name: 'image_url', value: expr('{{ $json.image_url }}') }, { name: 'is_carousel_item', value: 'true' }] }
    },
    credentials: { httpTemplatedCustomAuth: newCredential('Instagram token') }
  },
  output: [{ id: '17900000000000002' }]
});

const collectChildren = node({
  type: 'n8n-nodes-base.aggregate',
  version: 1,
  config: {
    name: 'Collect carousel children',
    parameters: { aggregate: 'aggregateAllItemData', destinationFieldName: 'children', include: 'allFields' }
  },
  output: [{ children: [{ id: '17900000000000002' }, { id: '17900000000000003' }] }]
});

const allChildrenOk = ifElse({
  version: 2.3,
  config: {
    name: 'All carousel images uploaded?',
    parameters: {
      conditions: {
        options: { caseSensitive: true, leftValue: '', typeValidation: 'loose' },
        conditions: [{ leftValue: expr('{{ $json.children.length >= 2 && $json.children.every(c => c.id && !c.error) }}'), operator: { type: 'boolean', operation: 'true', singleValue: true }, rightValue: '' }],
        combinator: 'and'
      },
      looseTypeValidation: true
    }
  }
});

const createCarousel = node({
  type: 'n8n-nodes-base.httpRequest',
  version: 4.5,
  config: {
    name: 'Create carousel container',
    onError: 'continueErrorOutput',
    parameters: {
      method: 'POST',
      url: "https://graph.instagram.com/v23.0/me/media",
      authentication: 'genericCredentialType',
      genericAuthType: 'httpTemplatedCustomAuth',
      sendBody: true,
      contentType: 'form-urlencoded',
      bodyParameters: { parameters: [{ name: 'media_type', value: 'CAROUSEL' }, { name: 'children', value: expr('{{ $json.children.map(c => c.id).join(",") }}') }, { name: 'caption', value: expr('{{ $("Prepare post").first().json.caption }}') }] }
    },
    credentials: { httpTemplatedCustomAuth: newCredential('Instagram token') }
  },
  output: [{ id: '17900000000000004' }]
});

const createReel = node({
  type: 'n8n-nodes-base.httpRequest',
  version: 4.5,
  config: {
    name: 'Create reel container',
    onError: 'continueErrorOutput',
    parameters: {
      method: 'POST',
      url: "https://graph.instagram.com/v23.0/me/media",
      authentication: 'genericCredentialType',
      genericAuthType: 'httpTemplatedCustomAuth',
      sendBody: true,
      contentType: 'form-urlencoded',
      bodyParameters: { parameters: [{ name: 'media_type', value: 'REELS' }, { name: 'video_url', value: expr('{{ $json.urls[0] }}') }, { name: 'caption', value: expr('{{ $json.caption }}') }, { name: 'share_to_feed', value: 'true' }] }
    },
    credentials: { httpTemplatedCustomAuth: newCredential('Instagram token') }
  },
  output: [{ id: '17900000000000005' }]
});

const waitForVideo = node({
  type: 'n8n-nodes-base.wait',
  version: 1.1,
  config: {
    name: 'Wait 10 seconds',
    parameters: { resume: 'timeInterval', amount: 10, unit: 'seconds' }
  },
  output: [{ id: '17900000000000005' }]
});

const checkReel = node({
  type: 'n8n-nodes-base.httpRequest',
  version: 4.5,
  config: {
    name: 'Check reel processing status',
    onError: 'continueErrorOutput',
    parameters: {
      method: 'GET',
      url: expr('https://graph.instagram.com/v23.0/{{ $("Create reel container").first().json.id }}'),
      authentication: 'genericCredentialType',
      genericAuthType: 'httpTemplatedCustomAuth',
      sendQuery: true,
      specifyQuery: 'keypair',
      queryParameters: { parameters: [{ name: 'fields', value: 'id,status_code' }] }
    },
    credentials: { httpTemplatedCustomAuth: newCredential('Instagram token') }
  },
  output: [{ id: '17900000000000005', status_code: 'FINISHED' }]
});

const reelState = switchCase({
  version: 3.4,
  config: {
    name: 'Reel ready?',
    parameters: {
      mode: 'rules',
      rules: {
        values: [
          { renameOutput: true, outputKey: 'Finished', conditions: { options: { caseSensitive: false, leftValue: '', typeValidation: 'strict' }, conditions: [{ leftValue: expr('{{ $json.status_code }}'), operator: { type: 'string', operation: 'equals' }, rightValue: 'FINISHED' }], combinator: 'and' } },
          { renameOutput: true, outputKey: 'Failed or timed out', conditions: { options: { caseSensitive: false, leftValue: '', typeValidation: 'loose' }, conditions: [{ leftValue: expr('{{ ["ERROR", "EXPIRED"].includes($json.status_code) || ($now.toMillis() - $("Prepare post").first().json.started_ms) > 300000 }}'), operator: { type: 'boolean', operation: 'true', singleValue: true }, rightValue: '' }], combinator: 'and' } }
        ]
      },
      looseTypeValidation: true,
      options: { fallbackOutput: 'extra', renameFallbackOutput: 'Still processing' }
    }
  }
});

const publishMedia = node({
  type: 'n8n-nodes-base.httpRequest',
  version: 4.5,
  config: {
    name: 'Publish to Instagram',
    onError: 'continueErrorOutput',
    parameters: {
      method: 'POST',
      url: "https://graph.instagram.com/v23.0/me/media_publish",
      authentication: 'genericCredentialType',
      genericAuthType: 'httpTemplatedCustomAuth',
      sendBody: true,
      contentType: 'form-urlencoded',
      bodyParameters: { parameters: [{ name: 'creation_id', value: expr('{{ $json.id }}') }] }
    },
    credentials: { httpTemplatedCustomAuth: newCredential('Instagram token') }
  },
  output: [{ id: '17900000000000099' }]
});

const getPermalink = node({
  type: 'n8n-nodes-base.httpRequest',
  version: 4.5,
  config: {
    name: 'Get post permalink',
    onError: 'continueRegularOutput',
    parameters: {
      method: 'GET',
      url: expr('https://graph.instagram.com/v23.0/{{ $json.id }}'),
      authentication: 'genericCredentialType',
      genericAuthType: 'httpTemplatedCustomAuth',
      sendQuery: true,
      specifyQuery: 'keypair',
      queryParameters: { parameters: [{ name: 'fields', value: 'id,permalink' }] }
    },
    credentials: { httpTemplatedCustomAuth: newCredential('Instagram token') }
  },
  output: [{ id: '17900000000000099', permalink: 'https://www.instagram.com/p/ABC123/' }]
});

const markPosted = node({
  type: 'n8n-nodes-base.googleSheets',
  version: 4.7,
  config: {
    name: 'Mark post as posted',
    parameters: {
      resource: 'sheet',
      operation: 'update',
      authentication: 'oAuth2',
      documentId: { __rl: true, mode: 'id', value: "1ARiXXigTeGEHhrLYptkGRec0JJAmgDw165fMRLeKjeA" },
      sheetName: { __rl: true, mode: 'name', value: 'Posts' },
      columns: {
        mappingMode: 'defineBelow',
        matchingColumns: ['id'],
        value: {
          id: expr('{{ $("Prepare post").first().json.row_id }}'),
          status: 'posted',
          ig_media_id: expr('{{ $("Publish to Instagram").first().json.id }}'),
          permalink: expr('{{ $json.permalink || "" }}'),
          error: ''
        },
        schema: [
          { id: 'id', displayName: 'id', required: false, defaultMatch: false, display: true, type: 'string', canBeUsedToMatch: true },
          { id: 'status', displayName: 'status', required: false, defaultMatch: false, display: true, type: 'string', canBeUsedToMatch: true },
          { id: 'ig_media_id', displayName: 'ig_media_id', required: false, defaultMatch: false, display: true, type: 'string', canBeUsedToMatch: true },
          { id: 'permalink', displayName: 'permalink', required: false, defaultMatch: false, display: true, type: 'string', canBeUsedToMatch: true },
          { id: 'error', displayName: 'error', required: false, defaultMatch: false, display: true, type: 'string', canBeUsedToMatch: true }
        ]
      },
      options: { cellFormat: 'RAW' }
    },
    credentials: { googleSheetsOAuth2Api: newCredential('Google Sheets (Instagram calendar)') }
  },
  output: [{ id: '2026-10-28-carousel', status: 'posted' }]
});

const describeFailure = node({
  type: 'n8n-nodes-base.set',
  version: 3.5,
  config: {
    name: 'Describe failure',
    parameters: {
      mode: 'manual',
      includeOtherFields: false,
      assignments: {
        assignments: [
          { id: 'fail-row', name: 'row_id', value: expr('{{ $("Prepare post").first().json.row_id }}'), type: 'string' },
          { id: 'fail-msg', name: 'error_message', value: expr("{{ $json.error ? ($json.error.message || $json.error.description || JSON.stringify($json.error)).slice(0, 300) : ($json.status_code ? ('Video processing ended with status ' + $json.status_code + ($json.status_code === 'IN_PROGRESS' ? ' (timed out after 5 min)' : '')) : ($json.children ? 'One or more carousel images failed to upload: ' + $json.children.filter(c => c.error).map(c => (c.error.message || 'error')).join('; ').slice(0, 250) : 'Unsupported format, or media_urls is empty. Use REEL, CAROUSEL or IMAGE.')) }}"), type: 'string' }
        ]
      }
    }
  },
  output: [{ row_id: '2026-10-28-carousel', error_message: 'Invalid image URL' }]
});

const markFailed = node({
  type: 'n8n-nodes-base.googleSheets',
  version: 4.7,
  config: {
    name: 'Mark post as failed',
    parameters: {
      resource: 'sheet',
      operation: 'update',
      authentication: 'oAuth2',
      documentId: { __rl: true, mode: 'id', value: "1ARiXXigTeGEHhrLYptkGRec0JJAmgDw165fMRLeKjeA" },
      sheetName: { __rl: true, mode: 'name', value: 'Posts' },
      columns: {
        mappingMode: 'defineBelow',
        matchingColumns: ['id'],
        value: {
          id: expr('{{ $json.row_id }}'),
          status: 'failed',
          error: expr('{{ $json.error_message }}')
        },
        schema: [
          { id: 'id', displayName: 'id', required: false, defaultMatch: false, display: true, type: 'string', canBeUsedToMatch: true },
          { id: 'status', displayName: 'status', required: false, defaultMatch: false, display: true, type: 'string', canBeUsedToMatch: true },
          { id: 'error', displayName: 'error', required: false, defaultMatch: false, display: true, type: 'string', canBeUsedToMatch: true }
        ]
      },
      options: { cellFormat: 'RAW' }
    },
    credentials: { googleSheetsOAuth2Api: newCredential('Google Sheets (Instagram calendar)') }
  },
  output: [{ id: '2026-10-28-carousel', status: 'failed' }]
});

const readReplies = node({
  type: 'n8n-nodes-base.googleSheets',
  version: 4.7,
  config: {
    name: 'Read Replies tab',
    parameters: {
      resource: 'sheet',
      operation: 'read',
      authentication: 'oAuth2',
      documentId: { __rl: true, mode: 'id', value: "1ARiXXigTeGEHhrLYptkGRec0JJAmgDw165fMRLeKjeA" },
      sheetName: { __rl: true, mode: 'name', value: 'Replies' },
      options: { outputFormatting: { values: { general: 'FORMATTED_VALUE', date: 'FORMATTED_STRING' } } }
    },
    credentials: { googleSheetsOAuth2Api: newCredential('Google Sheets (Instagram calendar)') }
  },
  output: [{ row_number: 2, comment_id: '17850000000000001', username: 'sara', draft_reply: 'Thanks, that matches what we see too.', status: 'approved' }]
});

const keepApprovedReplies = node({
  type: 'n8n-nodes-base.filter',
  version: 2.3,
  config: {
    name: 'Keep approved replies (not KEYWORD)',
    parameters: {
      conditions: {
        options: { caseSensitive: false, leftValue: '', typeValidation: 'loose' },
        conditions: [
          { leftValue: expr('{{ String($json.status || "").trim().toLowerCase() }}'), operator: { type: 'string', operation: 'equals' }, rightValue: 'approved' },
          { leftValue: expr('{{ String($json.comment_id || "").trim() }}'), operator: { type: 'string', operation: 'notEmpty', singleValue: true }, rightValue: '' },
          { leftValue: expr('{{ String($json.draft_reply || "").trim() }}'), operator: { type: 'string', operation: 'notEmpty', singleValue: true }, rightValue: '' },
          { leftValue: expr('{{ String($json.bucket || "").trim().toUpperCase() }}'), operator: { type: 'string', operation: 'notEquals' }, rightValue: 'KEYWORD' }
        ],
        combinator: 'and'
      },
      looseTypeValidation: true
    }
  },
  output: [{ row_number: 2, comment_id: '17850000000000001', username: 'sara', draft_reply: 'Thanks, that matches what we see too.', status: 'approved' }]
});

const loopReplies = splitInBatches({ version: 3, config: { name: 'One reply at a time', parameters: { batchSize: 1 } } });

const sendReply = node({
  type: 'n8n-nodes-base.httpRequest',
  version: 4.5,
  config: {
    name: 'Send reply under comment',
    onError: 'continueErrorOutput',
    parameters: {
      method: 'POST',
      url: expr('https://graph.instagram.com/v23.0/{{ String($json.comment_id).trim() }}/replies'),
      authentication: 'genericCredentialType',
      genericAuthType: 'httpTemplatedCustomAuth',
      sendBody: true,
      contentType: 'form-urlencoded',
      bodyParameters: { parameters: [{ name: 'message', value: expr('{{ $json.draft_reply }}') }] }
    },
    credentials: { httpTemplatedCustomAuth: newCredential('Instagram token') }
  },
  output: [{ id: '17850000000000099' }]
});

const markSent = node({
  type: 'n8n-nodes-base.googleSheets',
  version: 4.7,
  config: {
    name: 'Mark reply as sent',
    parameters: {
      resource: 'sheet',
      operation: 'update',
      authentication: 'oAuth2',
      documentId: { __rl: true, mode: 'id', value: "1ARiXXigTeGEHhrLYptkGRec0JJAmgDw165fMRLeKjeA" },
      sheetName: { __rl: true, mode: 'name', value: 'Replies' },
      columns: {
        mappingMode: 'defineBelow',
        matchingColumns: ['comment_id'],
        value: {
          comment_id: expr('{{ String($("One reply at a time").first().json.comment_id) }}'),
          status: 'sent',
          sent_at: expr('{{ $now.toISO() }}'),
          error: ''
        },
        schema: [
          { id: 'comment_id', displayName: 'comment_id', required: false, defaultMatch: false, display: true, type: 'string', canBeUsedToMatch: true },
          { id: 'status', displayName: 'status', required: false, defaultMatch: false, display: true, type: 'string', canBeUsedToMatch: true },
          { id: 'sent_at', displayName: 'sent_at', required: false, defaultMatch: false, display: true, type: 'string', canBeUsedToMatch: true },
          { id: 'error', displayName: 'error', required: false, defaultMatch: false, display: true, type: 'string', canBeUsedToMatch: true }
        ]
      },
      options: { cellFormat: 'RAW' }
    },
    credentials: { googleSheetsOAuth2Api: newCredential('Google Sheets (Instagram calendar)') }
  },
  output: [{ comment_id: '17850000000000001', status: 'sent' }]
});

const markReplyFailed = node({
  type: 'n8n-nodes-base.googleSheets',
  version: 4.7,
  config: {
    name: 'Mark reply as failed',
    parameters: {
      resource: 'sheet',
      operation: 'update',
      authentication: 'oAuth2',
      documentId: { __rl: true, mode: 'id', value: "1ARiXXigTeGEHhrLYptkGRec0JJAmgDw165fMRLeKjeA" },
      sheetName: { __rl: true, mode: 'name', value: 'Replies' },
      columns: {
        mappingMode: 'defineBelow',
        matchingColumns: ['comment_id'],
        value: {
          comment_id: expr('{{ String($("One reply at a time").first().json.comment_id) }}'),
          status: 'failed',
          error: expr('{{ ($json.error && ($json.error.message || JSON.stringify($json.error)) || "Unknown error").slice(0, 300) }}')
        },
        schema: [
          { id: 'comment_id', displayName: 'comment_id', required: false, defaultMatch: false, display: true, type: 'string', canBeUsedToMatch: true },
          { id: 'status', displayName: 'status', required: false, defaultMatch: false, display: true, type: 'string', canBeUsedToMatch: true },
          { id: 'error', displayName: 'error', required: false, defaultMatch: false, display: true, type: 'string', canBeUsedToMatch: true }
        ]
      },
      options: { cellFormat: 'RAW' }
    },
    credentials: { googleSheetsOAuth2Api: newCredential('Google Sheets (Instagram calendar)') }
  },
  output: [{ comment_id: '17850000000000001', status: 'failed' }]
});

const setupNote = sticky('## Setup before activating\n1. Create the **Instagram token** credential (Custom Auth template: header `Authorization: Bearer <long-lived token>`). Select it on all 8 HTTP nodes.\n2. Select your Google account on the 6 Google Sheets nodes (sheet: Instagram content calendar).\n3. Workflow settings > Timezone = Asia/Karachi.\n4. Only rows with status = approved and a date+time in the past are posted. media_urls must be public https links.\n5. Replies with bucket = KEYWORD are skipped (ManyChat handles those). comment_id column must be formatted as Plain text.', [], { color: 4 });

const reelLoop = reelState.onCase(0, publishMedia).onCase(1, describeFailure).onCase(2, waitForVideo);
const carouselCheck = allChildrenOk.onTrue(createCarousel.to(publishMedia)).onFalse(describeFailure);
const formatRouter = routeByFormat
  .onCase(0, createImage.to(publishMedia))
  .onCase(1, splitImages.to(createChild).to(collectChildren).to(carouselCheck))
  .onCase(2, createReel.to(waitForVideo).to(checkReel).to(reelLoop))
  .onCase(3, describeFailure);

export default workflow('ig-publisher', 'IG Publisher (approved posts + replies)')
  .add(everyFifteen)
  .to(readPosts)
  .to(keepDuePosts)
  .to(loopPosts.onEachBatch(preparePost.to(formatRouter)))
  .add(createImage.onError(describeFailure))
  .add(createCarousel.onError(describeFailure))
  .add(createReel.onError(describeFailure))
  .add(checkReel.onError(describeFailure))
  .add(publishMedia.to(getPermalink).to(markPosted).to(nextBatch(loopPosts)))
  .add(publishMedia.onError(describeFailure))
  .add(describeFailure.to(markFailed).to(nextBatch(loopPosts)))
  .add(everyFifteen)
  .to(readReplies)
  .to(keepApprovedReplies)
  .to(loopReplies.onEachBatch(sendReply.to(markSent).to(nextBatch(loopReplies))))
  .add(sendReply.onError(markReplyFailed.to(nextBatch(loopReplies))))
  .add(setupNote);
