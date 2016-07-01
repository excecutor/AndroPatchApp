.class public Lcom/vasts/JSinject;
.super Ljava/lang/Object;
.source "JSinject.java"


# direct methods
.method public constructor <init>()V
    .locals 0

    .prologue
    .line 7
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method

.method public static setInject(Landroid/webkit/WebView;)V
    .locals 1
    .param p0, "myWebView"    # Landroid/webkit/WebView;

    .prologue
    .line 9
    new-instance v0, Lcom/vasts/JSinject$1;

    invoke-direct {v0, p0}, Lcom/vasts/JSinject$1;-><init>(Landroid/webkit/WebView;)V

    invoke-virtual {p0, v0}, Landroid/webkit/WebView;->setWebViewClient(Landroid/webkit/WebViewClient;)V

    .line 24
    return-void
.end method
