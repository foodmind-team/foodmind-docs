# AWS record-image deployment checklist

- **Status:** Proposed deployment gate
- **Owner:** Backend / platform operator
- **Last updated:** 2026-08-16
- **Related repositories:** `foodmind-backend`, `foodmind-web`, `foodmind-android`, `foodmind-docs`
- **Scope:** Food and drink record images only

This checklist prepares the merged media feature for AWS. It does not authorize a deployment and it never requires committed AWS access keys.

## 1. Create a private S3 bucket

- Choose the application region and a globally unique bucket name.
- Enable all four S3 Block Public Access settings.
- Keep Object Ownership set to bucket-owner enforced; do not add a public bucket policy or ACL.
- Enable default encryption and the project's required versioning/logging controls.
- Keep the application key prefix at `media/` unless the IAM resource below is changed with it.
- Do not use a static website endpoint. Clients receive short-lived S3 presigned URLs.

Apply CORS with only the exact deployed Web origins. Replace the example origins before use:

```json
[
  {
    "AllowedOrigins": [
      "https://app.foodmind.example",
      "https://foodmind-web.vercel.app"
    ],
    "AllowedMethods": ["GET", "HEAD", "PUT"],
    "AllowedHeaders": [
      "Content-Type",
      "x-amz-checksum-sha256",
      "x-amz-sdk-checksum-algorithm",
      "x-amz-*"
    ],
    "ExposeHeaders": ["ETag", "x-amz-checksum-sha256"],
    "MaxAgeSeconds": 900
  }
]
```

Do not use `*` for a production origin. Android does not require browser CORS, but uses the same private presigned URLs.

## 2. Grant the ECS task role least privilege

Attach object access to the Backend **task role**, not the ECS task execution role. Replace the bucket name and keep the resource limited to the configured key prefix:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "FoodMindRecordMediaObjects",
      "Effect": "Allow",
      "Action": [
        "s3:PutObject",
        "s3:GetObject",
        "s3:DeleteObject"
      ],
      "Resource": "arn:aws:s3:::REPLACE_WITH_BUCKET/media/*"
    }
  ]
}
```

The task role trust policy must allow `ecs-tasks.amazonaws.com`. Do not create or inject an IAM user's access key. Confirm with IAM Access Analyzer or an equivalent review that the role cannot access unrelated buckets or prefixes.

## 3. Configure the Backend task definition

Set these runtime values only after the bucket, CORS, and task role are ready:

| Variable | Production value |
| --- | --- |
| `MEDIA_ENABLED` | `true` |
| `MEDIA_S3_BUCKET` | Private bucket name |
| `MEDIA_S3_REGION` | Bucket region, for example `ap-southeast-1` |
| `MEDIA_S3_ENDPOINT` | Empty/unset on AWS |
| `MEDIA_S3_PUBLIC_ENDPOINT` | Empty/unset on AWS |
| `MEDIA_S3_KEY_PREFIX` | `media` |
| `MEDIA_UPLOAD_TTL` | `5m` |
| `MEDIA_READ_TTL` | `15m` |
| `MEDIA_MAX_BYTE_SIZE` | `5242880` |
| `MEDIA_CLEANUP_DELAY` | At least `15m` |

Leave `MEDIA_S3_ACCESS_KEY` and `MEDIA_S3_SECRET_KEY` empty/unset so the AWS SDK uses the ECS task-role credential provider. A custom endpoint is only for local S3-compatible storage such as MinIO.

Deploy the Flyway migration before allowing client traffic. Check Backend readiness and logs for credential, region, bucket, checksum, and signing errors without logging signed URLs.

## 4. Configure Web delivery

Set `FOODMIND_MEDIA_ORIGIN` to the one exact virtual-hosted S3 origin used by presigned URLs, for example:

```text
https://REPLACE_WITH_BUCKET.s3.ap-southeast-1.amazonaws.com
```

The value must be HTTPS and must not contain a path, query, credentials, wildcard, or trailing slash. The Web CSP then allows `blob:` for local preview and that exact S3 origin for PUT and image reads. Bearer tokens remain restricted to the Backend; S3 requests use only the query signature.

Rebuild/redeploy the Web artifact after changing this value. Confirm the production response CSP does not broaden `connect-src` or `img-src` to arbitrary AWS hosts.

## 5. Release and smoke-test sequence

1. Merge and deploy Backend, then Web, then Android using the reviewed commits.
2. With a test owner, upload a valid JPEG, PNG, and WebP below 5 MB.
3. Confirm the object stays private and the database transitions `PENDING -> READY`.
4. Confirm the saved image loads in Web record detail, Web Explore card/preview, Android record detail, and Android Explore.
5. Confirm a replacement removes the superseded asset and a failed record save removes the newly uploaded asset.
6. With a user outside the trusted group, confirm record detail is denied and Search/Explore do not return an image URL.
7. Confirm deleted, unfinished, non-READY, and unauthorised attachments return `null`, never an object key.
8. Confirm a read URL expires near the configured 15-minute TTL and a refreshed API response supplies a new URL.
9. Inspect S3 data events/application logs as permitted, without copying presigned query strings into evidence.

## 6. Rollback

Set `MEDIA_ENABLED=false` to stop new declarations and URL signing while retaining private objects and record metadata. Roll back clients independently if required. Do not make the bucket public as a workaround. Investigate and clean orphaned test assets through the application-owned deletion path before re-enabling.

## AWS references

- [ECS task IAM roles](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-iam-roles.html)
- [S3 presigned URLs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-presigned-url.html)
- [S3 CORS configuration](https://docs.aws.amazon.com/AmazonS3/latest/userguide/ManageCorsUsing.html)
- [S3 Block Public Access](https://docs.aws.amazon.com/AmazonS3/latest/userguide/access-control-block-public-access.html)
